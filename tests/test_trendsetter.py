import pytest
from src.trendsetter import Trendsetter
import pandas
# from pandas.testing import assert_frame_equal

@pytest.fixture
def trendsetter():
    return Trendsetter()

def test_browse_categories(trendsetter):
    # assert assert_frame_equal(trendsetter.browse_categories([6,7]),
                              # pandas.DataFrame([['Commodities & Futures Trading', 904]], columns=['name', 'id']))
    assert trendsetter.browse_categories([6,7]).equals(pandas.DataFrame([['Commodities & Futures Trading', 904]], columns=['name', 'id']))

def test_browse_categories_return_nothing(trendsetter):
    assert trendsetter.browse_categories([6,7,0]) == None

# def test_get_trending_country_code(trendsetter):
#     assert isinstance(trendsetter.get_trending('DE'),

def test_get_trending_country_code_error(trendsetter):
    with pytest.raises(ValueError) as err:
        trendsetter.get_trending('XX')
    assert "Country not supported." in str(err.value)

def test_get_related(trendsetter):
    pass

def test_get_interest(trendsetter):
    pass
