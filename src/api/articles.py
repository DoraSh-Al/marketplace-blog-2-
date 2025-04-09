from datetime import datetime

from fastapi import APIRouter, HTTPException

from src.schemas.article import ArticleCreate, ArticleOut, ArticleUpdate

router = APIRouter(prefix="/articles", tags=["articles"])

# Временное хранилище статей
fake_articles_db = {}

@router.post("/", response_model=ArticleOut)
def create_article(article: ArticleCreate):
    article_id = len(fake_articles_db) + 1
    new_article = {
        "id": article_id,
        "title": article.title,
        "content": article.content,
        "category_id": article.category_id,
        "image_url": article.image_url,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
    fake_articles_db[article_id] = new_article
    return new_article

@router.get("/{article_id}", response_model=ArticleOut)
def read_article(article_id: int):
    article = fake_articles_db.get(article_id)
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    return article

@router.put("/{article_id}", response_model=ArticleOut)
def update_article(article_id: int, article: ArticleUpdate):
    db_article = fake_articles_db.get(article_id)
    if not db_article:
        raise HTTPException(status_code=404, detail="Article not found")
    update_data = article.dict(exclude_unset=True)
    update_data["updated_at"] = datetime.utcnow()
    fake_articles_db[article_id] = {**db_article, **update_data}
    return fake_articles_db[article_id]

@router.delete("/{article_id}")
def delete_article(article_id: int):
    if article_id not in fake_articles_db:
        raise HTTPException(status_code=404, detail="Article not found")
    del fake_articles_db[article_id]
    return {"message": "Article deleted"}
