from fastapi import APIRouter

router = APIRouter()


@router.get("/structure")
async def language_structure():
    return {
        "structure": [
            "Language/",
            "  Vocabulary/",
            "  Grammar/",
            "  Word Formation/",
            "  Rules/",
            "  References/",
            "  Drafts/",
        ]
    }
