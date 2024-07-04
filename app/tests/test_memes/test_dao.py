"""
В этих тестах я тестировал CRUD операции с мемами
"""
import pytest

from app.memes.dao import MemDAO

LIMIT_RECORDS = 100


@pytest.mark.parametrize("description, file_name, mem_id", [
    (f"Мем {i}", f"Картинка_мем_{i}", i) for i in range(1, LIMIT_RECORDS)
])
async def test_create_memes(description, file_name, mem_id):
    returning_mem_id = await MemDAO.add(description=description, file_name=file_name)

    assert returning_mem_id == mem_id


@pytest.mark.parametrize("mem_id", [i for i in range(1, LIMIT_RECORDS)])
async def test_read_memes(mem_id):
    returning_mem = await MemDAO.get_by_id(mem_id)

    assert returning_mem.id == mem_id


@pytest.mark.parametrize("new_description, new_file_name, mem_id", [
    (f"Новый мем {i}", f"Новая_картинка_мема_{i}", i) for i in range(1, LIMIT_RECORDS)
])
async def test_update_memes(new_description, new_file_name, mem_id):
    returning_mem = await MemDAO.update(model_id=mem_id,
                                           description=new_description,
                                           file_name=new_file_name)

    assert returning_mem.id == mem_id
    assert returning_mem.description == new_description
    assert returning_mem.file_name == new_file_name


@pytest.mark.parametrize("mem_id", [i for i in range(1, LIMIT_RECORDS)])
async def test_delete_memes(mem_id):
    returning_mem = await MemDAO.delete_by_id(mem_id)

    assert returning_mem.id == mem_id
