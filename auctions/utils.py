# File with Useful Functions
from .models import CATEGORIES_CHOICES

# CREATE CATEGORY LIST FUNCTION STARTS
def CreateCategoriesList():
    categoriesList = []

    for category in CATEGORIES_CHOICES:
        categoriesList.append(category[0])

    return categoriesList
# CREATE CATEGORY LIST FUNCTION ENDS