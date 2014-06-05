import pytest
from mock import Mock, MagicMock, patch
from trellis import Trellis
import settings


@pytest.fixture
def trellis_obj():
    return Trellis(Mock(), Mock(), Mock())


@patch('trellis.Trellis.get_lists')
def test_get_list_id_from_name_works(mock_get_lists, trellis_obj):
    mock_get_lists.return_value = [{'id': 'eh23jnd2', 'name': 'Thang'}]
    list_id = trellis_obj._get_list_id_from_name("Thang")
    assert list_id == 'eh23jnd2'


@patch('trellis.Trellis.get_lists')
def test_get_list_id_from_name_is_none_with_nonexistent_name(mock_get_lists,
                                                             trellis_obj):
    mock_get_lists.return_value = [{'id': 'eh23jnd2', 'name': 'Thang'}]
    list_id = trellis_obj._get_list_id_from_name("NotThang")
    assert not list_id


@patch('trellis.requests.get')
def test_get_lists(mock_get, trellis_obj):
    trellis_obj.get_lists()
    mock_get.assert_called_with(settings.BOARD_URL.format(trellis_obj.board_id,
                                                          trellis_obj.app_key,
                                                          trellis_obj.app_token))


@patch('trellis.requests.get')
def test_get_list_data(mock_get, trellis_obj):
    trellis_obj.get_list_data('listylist')
    mock_get.assert_called_with(settings.LIST_URL.format('listylist',
                                                         trellis_obj.app_key,
                                                         trellis_obj.app_token))


@patch('trellis.grequests')
def test_get_history_for_cards(mock_g, trellis_obj):
    trellis_obj._get_history_for_cards(MagicMock(spec=dict))
    assert mock_g.map.called


def test_repr(trellis_obj):
    assert repr(trellis_obj).startswith('<Trellis')
