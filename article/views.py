from django.db.models import Q, Count
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator, EmptyPage

from rest_framework import permissions, status
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser

from .models import Article, ArticleCategory, MediaFile
from .serializers import (
    ArticleSerializer,
    ArticleCreateUpdateSerializer,
    ArticleCategorySerializer,
    MediaUploadSerializer,
)
from .utils import (
    success_response,
    error_response,
    is_admin,
    is_admin_or_editor,
    get_user_role,
)


def check_xsrf_header(request):
    """
    Optional strict check.
    If you want to enforce it strictly, uncomment the header checks.
    """
    # token = request.headers.get("X-XSRF-Token")
    # return bool(token)
    return True


def filter_articles_by_visibility(request, queryset):
    """
    Public users -> published only
    Admin -> all
    Editor -> published + own articles
    """
    if not request.user.is_authenticated:
        return queryset.filter(status="published")

    role = get_user_role(request.user)

    if role == "admin":
        return queryset

    if role == "editor":
        return queryset.filter(Q(status="published") | Q(author=request.user))

    return queryset.filter(status="published")


def paginate_queryset(queryset, page, per_page):
    paginator = Paginator(queryset, per_page)
    try:
        page_obj = paginator.page(page)
    except EmptyPage:
        return None, {
            "page": ["Invalid page number"]
        }

    meta = {
        "current_page": page_obj.number,
        "per_page": per_page,
        "total": paginator.count,
        "total_pages": paginator.num_pages,
    }
    return page_obj, meta


# =========================
# CATEGORY ENDPOINTS
# =========================

@api_view(["GET"])
@permission_classes([permissions.AllowAny])
def category_list(request):
    categories = ArticleCategory.objects.annotate(
        article_count=Count("articles")
    ).order_by("name")

    serializer = ArticleCategorySerializer(categories, many=True)
    return success_response("Categories retrieved successfully", serializer.data)


@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def category_create(request):
    if not check_xsrf_header(request):
        return error_response(
            "Authentication required",
            "AUTH_REQUIRED",
            status_code=403
        )

    if not is_admin_or_editor(request.user):
        return error_response(
            "Insufficient permissions",
            "PERMISSION_DENIED",
            status_code=403
        )

    serializer = ArticleCategorySerializer(data=request.data)
    if serializer.is_valid():
        category = serializer.save()
        output = ArticleCategorySerializer(category)
        return success_response(
            "Category created successfully",
            output.data,
            status_code=status.HTTP_201_CREATED
        )

    return error_response(
        "Validation failed",
        "VALIDATION_ERROR",
        serializer.errors,
        status_code=400
    )


@api_view(["GET"])
@permission_classes([permissions.AllowAny])
def category_detail(request, slug):
    category = get_object_or_404(
        ArticleCategory.objects.annotate(article_count=Count("articles")),
        slug=slug
    )

    queryset = Article.objects.select_related("category", "author").filter(category=category)
    queryset = filter_articles_by_visibility(request, queryset)

    status_filter = request.GET.get("status")
    page = int(request.GET.get("page", 1))
    per_page = min(int(request.GET.get("per_page", 10)), 100)

    if status_filter:
        queryset = queryset.filter(status=status_filter)

    page_obj, meta = paginate_queryset(queryset, page, per_page)
    if page_obj is None:
        return error_response(
            "Validation failed",
            "VALIDATION_ERROR",
            meta,
            status_code=400
        )

    article_serializer = ArticleSerializer(
        page_obj.object_list,
        many=True,
        context={"request": request}
    )

    data = {
        "id": category.id,
        "name": category.name,
        "slug": category.slug,
        "description": category.description,
        "article_count": queryset.count(),
        "articles": article_serializer.data,
        "meta": meta
    }

    return success_response("Category retrieved successfully", data)


@api_view(["PUT", "PATCH"])
@permission_classes([permissions.IsAuthenticated])
def category_update(request, slug):
    if not check_xsrf_header(request):
        return error_response(
            "Authentication required",
            "AUTH_REQUIRED",
            status_code=403
        )

    if not is_admin_or_editor(request.user):
        return error_response(
            "Insufficient permissions",
            "PERMISSION_DENIED",
            status_code=403
        )

    category = get_object_or_404(ArticleCategory, slug=slug)

    serializer = ArticleCategorySerializer(category, data=request.data, partial=True)
    if serializer.is_valid():
        category = serializer.save()
        output = ArticleCategorySerializer(category)
        return success_response("Category updated successfully", output.data)

    return error_response(
        "Validation failed",
        "VALIDATION_ERROR",
        serializer.errors,
        status_code=400
    )


@api_view(["DELETE"])
@permission_classes([permissions.IsAuthenticated])
def category_delete(request, slug):
    if not check_xsrf_header(request):
        return error_response(
            "Authentication required",
            "AUTH_REQUIRED",
            status_code=403
        )

    if not is_admin(request.user):
        return error_response(
            "Insufficient permissions",
            "PERMISSION_DENIED",
            status_code=403
        )

    category = get_object_or_404(ArticleCategory, slug=slug)

    if category.articles.exists():
        return error_response(
            "Category cannot be deleted because it has articles",
            "VALIDATION_ERROR",
            {"category": ["Delete or move related articles first."]},
            status_code=400
        )

    category.delete()
    return success_response("Category deleted successfully", data=None)


# =========================
# ARTICLE ENDPOINTS
# =========================

@api_view(["GET"])
@permission_classes([permissions.AllowAny])
def blog_list(request):
    queryset = Article.objects.select_related("category", "author").all()
    queryset = filter_articles_by_visibility(request, queryset)

    category = request.GET.get("category")
    status_filter = request.GET.get("status")
    search = request.GET.get("search")
    page = int(request.GET.get("page", 1))
    per_page = min(int(request.GET.get("per_page", 10)), 100)
    sort = request.GET.get("sort", "date")
    order = request.GET.get("order", "desc")

    if category:
        queryset = queryset.filter(category__slug=category)

    if status_filter:
        queryset = queryset.filter(status=status_filter)

    if search:
        queryset = queryset.filter(
            Q(title__icontains=search) |
            Q(content__icontains=search) |
            Q(excerpt__icontains=search)
        )

    sort_map = {
        "date": "created_at",
        "title": "title",
        "status": "status",
    }

    sort_field = sort_map.get(sort, "created_at")
    if order == "desc":
        sort_field = f"-{sort_field}"

    queryset = queryset.order_by(sort_field)

    page_obj, meta = paginate_queryset(queryset, page, per_page)
    if page_obj is None:
        return error_response(
            "Validation failed",
            "VALIDATION_ERROR",
            meta,
            status_code=400
        )

    serializer = ArticleSerializer(
        page_obj.object_list,
        many=True,
        context={"request": request}
    )

    return success_response(
        "Articles retrieved successfully",
        serializer.data,
        meta=meta
    )


@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def blog_create(request):
    if not check_xsrf_header(request):
        return error_response(
            "Authentication required",
            "AUTH_REQUIRED",
            status_code=403
        )

    if not is_admin_or_editor(request.user):
        return error_response(
            "Insufficient permissions",
            "PERMISSION_DENIED",
            status_code=403
        )

    serializer = ArticleCreateUpdateSerializer(
        data=request.data,
        context={"request": request}
    )
    if serializer.is_valid():
        article = serializer.save(author=request.user)
        output = ArticleSerializer(article, context={"request": request})
        return success_response(
            "Article created successfully",
            output.data,
            status_code=status.HTTP_201_CREATED
        )

    return error_response(
        "Validation failed",
        "VALIDATION_ERROR",
        serializer.errors,
        status_code=400
    )


@api_view(["GET"])
@permission_classes([permissions.AllowAny])
def blog_detail(request, slug):
    queryset = Article.objects.select_related("category", "author").all()
    queryset = filter_articles_by_visibility(request, queryset)

    article = get_object_or_404(queryset, slug=slug)
    serializer = ArticleSerializer(article, context={"request": request})
    return success_response("Article retrieved successfully", serializer.data)


@api_view(["PUT", "PATCH"])
@permission_classes([permissions.IsAuthenticated])
def blog_update(request, slug):
    if not check_xsrf_header(request):
        return error_response(
            "Authentication required",
            "AUTH_REQUIRED",
            status_code=403
        )

    article = get_object_or_404(Article, slug=slug)

    if is_admin(request.user):
        pass
    elif is_admin_or_editor(request.user):
        if article.author != request.user:
            return error_response(
                "Insufficient permissions",
                "PERMISSION_DENIED",
                status_code=403
            )
    else:
        return error_response(
            "Insufficient permissions",
            "PERMISSION_DENIED",
            status_code=403
        )

    serializer = ArticleCreateUpdateSerializer(
        article,
        data=request.data,
        partial=True,
        context={"request": request}
    )

    if serializer.is_valid():
        article = serializer.save()
        output = ArticleSerializer(article, context={"request": request})
        return success_response("Article updated successfully", output.data)

    return error_response(
        "Validation failed",
        "VALIDATION_ERROR",
        serializer.errors,
        status_code=400
    )


@api_view(["DELETE"])
@permission_classes([permissions.IsAuthenticated])
def blog_delete(request, slug):
    if not check_xsrf_header(request):
        return error_response(
            "Authentication required",
            "AUTH_REQUIRED",
            status_code=403
        )

    article = get_object_or_404(Article, slug=slug)

    if is_admin(request.user):
        pass
    elif is_admin_or_editor(request.user):
        if article.author != request.user:
            return error_response(
                "Insufficient permissions",
                "PERMISSION_DENIED",
                status_code=403
            )
    else:
        return error_response(
            "Insufficient permissions",
            "PERMISSION_DENIED",
            status_code=403
        )

    article.delete()
    return success_response("Article deleted successfully", data=None)


# =========================
# MEDIA ENDPOINT
# =========================

@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def media_upload(request):
    if not check_xsrf_header(request):
        return error_response(
            "Authentication required",
            "AUTH_REQUIRED",
            status_code=403
        )

    if not is_admin_or_editor(request.user):
        return error_response(
            "Insufficient permissions",
            "PERMISSION_DENIED",
            status_code=403
        )

    file = request.FILES.get("file")
    media_type = request.data.get("type")

    if not file:
        return error_response(
            "Validation failed",
            "VALIDATION_ERROR",
            {"file": ["This field is required."]},
            status_code=400
        )

    allowed_types = ["image/jpeg", "image/png", "image/gif", "image/webp"]
    max_size = 5 * 1024 * 1024

    if file.content_type not in allowed_types:
        return error_response(
            "Invalid file type",
            "INVALID_FILE_TYPE",
            {"file": ["Allowed formats: JPEG, PNG, GIF, WebP"]},
            status_code=422
        )

    if file.size > max_size:
        return error_response(
            "File exceeds size limit",
            "FILE_TOO_LARGE",
            {"file": ["Maximum allowed size is 5MB"]},
            status_code=413
        )

    if media_type not in ["featured", "attachment"]:
        return error_response(
            "Validation failed",
            "VALIDATION_ERROR",
            {"type": ["Type must be either 'featured' or 'attachment'."]},
            status_code=400
        )

    media = MediaFile.objects.create(
        file=file,
        original_name=file.name,
        mime_type=file.content_type,
        size=file.size,
        type=media_type
    )

    serializer = MediaUploadSerializer(media, context={"request": request})
    return success_response(
        "Media uploaded successfully",
        serializer.data,
        status_code=status.HTTP_201_CREATED
    )