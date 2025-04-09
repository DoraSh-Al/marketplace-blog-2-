from datetime import datetime
from typing import List

from fastapi import APIRouter, Body, Depends, HTTPException, Query
from sqlalchemy import text
from sqlalchemy.orm import Session

from src.models.article import Article
from src.models.database import get_db
from src.models.deleted_article import DeletedArticle
from src.schemas.article import ArticleCreate, ArticleOut, ArticleUpdate

router = APIRouter(prefix="/articles", tags=["articles"])

@router.post("/", response_model=ArticleOut)
def create_article(
    article: ArticleCreate = Body(...),  # Явно указываем тело
    db: Session = Depends(get_db)
):
    new_article = Article(
        title=article.title,
        content=article.content,
        category_id=article.category_id,
        image_url=None
    )
    db.add(new_article)
    db.commit()
    db.refresh(new_article)
    return new_article

@router.get("/", response_model=List[ArticleOut])  # Список статей
def get_articles(
    search: str = Query(None, description="Search term for title or content"),
    category_id: int = Query(None, description="Filter by category ID"),
    page_number: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(10, ge=1, le=100, description="Items per page"),
    db: Session = Depends(get_db)
):
    query = db.query(Article)

    # Фильтр по категории
    if category_id:
        query = query.filter(Article.category_id == category_id)

    # Полнотекстовый поиск
    if search:
        query = query.filter(
            text("to_tsvector('russian', title || ' ' || content) @@ to_tsquery('russian', :search)")
        ).params(search=search.replace(" ", " & "))

    # Пагинация
    query.count()
    query = query.offset((page_number - 1) * page_size).limit(page_size)
    articles = query.all()

    return articles

@router.get("/{article_id}", response_model=ArticleOut)  # Одна статья
def read_article(article_id: int, db: Session = Depends(get_db)):
    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    return article

@router.put("/{article_id}", response_model=ArticleOut)
def update_article(article_id: int, article: ArticleUpdate, db: Session = Depends(get_db)):
    db_article = db.query(Article).filter(Article.id == article_id).first()
    if not db_article:
        raise HTTPException(status_code=404, detail="Article not found")
    update_data = article.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_article, key, value)
    db_article.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_article)
    return db_article

@router.delete("/{article_id}")
def delete_article(article_id: int, db: Session = Depends(get_db)):
    db_article = db.query(Article).filter(Article.id == article_id).first()
    if not db_article:
        raise HTTPException(status_code=404, detail="Article not found")

    # Фейковое удаление: переносим в deleted_articles
    deleted_article = DeletedArticle(
        article_id=db_article.id,
        title=db_article.title,
        content=db_article.content,
        category_id=db_article.category_id,
        image_url=db_article.image_url
    )
    db.add(deleted_article)
    db.delete(db_article)
    db.commit()
    return {"message": "Article moved to deleted_articles"}
