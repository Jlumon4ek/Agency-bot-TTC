from typing import List, Any, TypeVar, Generic, Optional, Dict
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.future import select
from sqlalchemy import update as sqlalchemy_update, delete as sqlalchemy_delete, func
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from dao import BaseModel as Base, get_session

T = TypeVar("T", bound=Base)

def remove_none_values(data: Dict) -> Dict:
    """Возвращает копию словаря без значений None."""
    return {k: v for k, v in data.items() if v is not None}

class BaseDAO(Generic[T]):
    model: type[T]

    @classmethod
    async def find_one_or_none_by_id(cls, data_id: int, session: Optional[AsyncSession] = None) -> Optional[T]:
        if session is None:
            async with get_session() as session:
                return await cls.find_one_or_none_by_id(data_id, session=session)

        logger.info(f"Поиск {cls.model.__name__} с ID: {data_id}")
        try:
            query = select(cls.model).filter_by(id=data_id)
            result = await session.execute(query)
            record = result.scalar_one_or_none()
            if record:
                logger.info(f"Запись с ID {data_id} найдена.")
            else:
                logger.info(f"Запись с ID {data_id} не найдена.")
            return record
        except SQLAlchemyError as e:
            logger.error(f"Ошибка при поиске записи с ID {data_id}: {e}")
            raise

    @classmethod
    async def find_one_or_none(cls, filters: Dict, session: Optional[AsyncSession] = None) -> Optional[T]:
        if session is None:
            async with get_session() as session:
                return await cls.find_one_or_none(filters, session=session)

        filter_dict = remove_none_values(filters) if filters else {}
        logger.info(f"Поиск одной записи {cls.model.__name__} по фильтрам: {filter_dict}")
        try:
            query = select(cls.model).filter_by(**filter_dict)
            result = await session.execute(query)
            record = result.scalar_one_or_none()
            if record:
                logger.info(f"Запись найдена по фильтрам: {filter_dict}")
            else:
                logger.info(f"Запись не найдена по фильтрам: {filter_dict}")
            return record
        except SQLAlchemyError as e:
            logger.error(f"Ошибка при поиске записи по фильтрам {filter_dict}: {e}")
            raise

    @classmethod
    async def find_all(cls, filters: Optional[Dict] = None, session: Optional[AsyncSession] = None) -> List[T]:
        if session is None:
            async with get_session() as session:
                return await cls.find_all(filters, session=session)

        filter_dict = remove_none_values(filters) if filters else {}
        logger.info(f"Поиск всех записей {cls.model.__name__} по фильтрам: {filter_dict}")
        try:
            query = select(cls.model).filter_by(**filter_dict)
            result = await session.execute(query)
            records = result.scalars().all()
            logger.info(f"Найдено {len(records)} записей.")
            return records
        except SQLAlchemyError as e:
            logger.error(f"Ошибка при поиске всех записей по фильтрам {filter_dict}: {e}")
            raise

    @classmethod
    async def add(cls, values: Dict, session: Optional[AsyncSession] = None) -> T:
        if session is None:
            async with get_session() as session:
                return await cls.add(values, session=session)

        values_dict = remove_none_values(values)
        logger.info(f"Добавление записи {cls.model.__name__} с параметрами: {values_dict}")
        new_instance = cls.model(**values_dict)
        session.add(new_instance)
        try:
            await session.flush()
            logger.info(f"Запись {cls.model.__name__} успешно добавлена.")
        except SQLAlchemyError as e:
            await session.rollback()
            logger.error(f"Ошибка при добавлении записи: {e}")
            raise e
        return new_instance

    @classmethod
    async def add_many(cls, instances: List[Dict], session: Optional[AsyncSession] = None) -> List[T]:
        if session is None:
            async with get_session() as session:
                return await cls.add_many(instances, session=session)

        logger.info(f"Добавление нескольких записей {cls.model.__name__}. Количество: {len(instances)}")
        new_instances = [cls.model(**remove_none_values(item)) for item in instances]
        session.add_all(new_instances)
        try:
            await session.flush()
            logger.info(f"Успешно добавлено {len(new_instances)} записей.")
        except SQLAlchemyError as e:
            await session.rollback()
            logger.error(f"Ошибка при добавлении нескольких записей: {e}")
            raise e
        return new_instances

    @classmethod
    async def update(cls, filters: Dict, values: Dict, session: Optional[AsyncSession] = None) -> int:
        if session is None:
            async with get_session() as session:
                return await cls.update(filters, values, session=session)

        filter_dict = remove_none_values(filters)
        values_dict = remove_none_values(values)
        logger.info(f"Обновление записей {cls.model.__name__} по фильтру: {filter_dict} с параметрами: {values_dict}")
        query = (
            sqlalchemy_update(cls.model)
            .where(*[getattr(cls.model, k) == v for k, v in filter_dict.items()])
            .values(**values_dict)
            .execution_options(synchronize_session="fetch")
        )
        try:
            result = await session.execute(query)
            await session.flush()
            logger.info(f"Обновлено {result.rowcount} записей.")
            return result.rowcount
        except SQLAlchemyError as e:
            await session.rollback()
            logger.error(f"Ошибка при обновлении записей: {e}")
            raise e

    @classmethod
    async def delete(cls, filters: Dict, session: Optional[AsyncSession] = None) -> int:
        if session is None:
            async with get_session() as session:
                return await cls.delete(filters, session=session)

        filter_dict = remove_none_values(filters)
        logger.info(f"Удаление записей {cls.model.__name__} по фильтру: {filter_dict}")
        if not filter_dict:
            logger.error("Нужен хотя бы один фильтр для удаления.")
            raise ValueError("Нужен хотя бы один фильтр для удаления.")

        query = sqlalchemy_delete(cls.model).filter_by(**filter_dict)
        try:
            result = await session.execute(query)
            await session.flush()
            logger.info(f"Удалено {result.rowcount} записей.")
            return result.rowcount
        except SQLAlchemyError as e:
            await session.rollback()
            logger.error(f"Ошибка при удалении записей: {e}")
            raise e

    @classmethod
    async def count(cls, filters: Optional[Dict] = None, session: Optional[AsyncSession] = None) -> int:
        if session is None:
            async with get_session() as session:
                return await cls.count(filters, session=session)

        filter_dict = remove_none_values(filters) if filters else {}
        logger.info(f"Подсчет количества записей {cls.model.__name__} по фильтру: {filter_dict}")
        try:
            query = select(func.count(cls.model.id)).filter_by(**filter_dict)
            result = await session.execute(query)
            count = result.scalar()
            logger.info(f"Найдено {count} записей.")
            return count
        except SQLAlchemyError as e:
            logger.error(f"Ошибка при подсчете записей: {e}")
            raise

    @classmethod
    async def paginate(
        cls,
        page: int = 1,
        page_size: int = 10,
        filters: Optional[Dict] = None,
        session: Optional[AsyncSession] = None,
    ) -> List[T]:
        if session is None:
            async with get_session() as session:
                return await cls.paginate(page, page_size, filters, session=session)

        filter_dict = remove_none_values(filters) if filters else {}
        logger.info(
            f"Пагинация записей {cls.model.__name__} по фильтру: {filter_dict}, страница: {page}, размер страницы: {page_size}"
        )
        try:
            query = select(cls.model).filter_by(**filter_dict)
            result = await session.execute(query.offset((page - 1) * page_size).limit(page_size))
            records = result.scalars().all()
            logger.info(f"Найдено {len(records)} записей на странице {page}.")
            return records
        except SQLAlchemyError as e:
            logger.error(f"Ошибка при пагинации записей: {e}")
            raise

    @classmethod
    async def find_by_ids(cls, ids: List[int], session: Optional[AsyncSession] = None) -> List[Any]:
        if session is None:
            async with get_session() as session:
                return await cls.find_by_ids(ids, session=session)

        logger.info(f"Поиск записей {cls.model.__name__} по списку ID: {ids}")
        try:
            query = select(cls.model).filter(cls.model.id.in_(ids))
            result = await session.execute(query)
            records = result.scalars().all()
            logger.info(f"Найдено {len(records)} записей по списку ID.")
            return records
        except SQLAlchemyError as e:
            logger.error(f"Ошибка при поиске записей по списку ID: {e}")
            raise

    @classmethod
    async def upsert(cls, unique_fields: List[str], values: Dict, session: Optional[AsyncSession] = None) -> T:
        if session is None:
            async with get_session() as session:
                return await cls.upsert(unique_fields, values, session=session)

        values_dict = remove_none_values(values)
        filter_dict = {field: values_dict[field] for field in unique_fields if field in values_dict}

        logger.info(f"Upsert для {cls.model.__name__} с фильтром: {filter_dict}")
        try:
            existing = await cls.find_one_or_none(filter_dict, session=session)
            if existing:
                for key, value in values_dict.items():
                    setattr(existing, key, value)
                await session.flush()
                logger.info(f"Обновлена существующая запись {cls.model.__name__}")
                return existing
            else:
                new_instance = cls.model(**values_dict)
                session.add(new_instance)
                await session.flush()
                logger.info(f"Создана новая запись {cls.model.__name__}")
                return new_instance
        except SQLAlchemyError as e:
            await session.rollback()
            logger.error(f"Ошибка при upsert: {e}")
            raise e

    @classmethod
    async def bulk_update(cls, records: List[Dict], session: Optional[AsyncSession] = None) -> int:
        if session is None:
            async with get_session() as session:
                return await cls.bulk_update(records, session=session)

        logger.info(f"Массовое обновление записей {cls.model.__name__}")
        try:
            updated_count = 0
            for record in records:
                record_dict = remove_none_values(record)
                if 'id' not in record_dict:
                    continue

                update_data = {k: v for k, v in record_dict.items() if k != 'id'}
                stmt = (
                    sqlalchemy_update(cls.model)
                    .filter_by(id=record_dict['id'])
                    .values(**update_data)
                )
                result = await session.execute(stmt)
                updated_count += result.rowcount

            await session.flush()
            logger.info(f"Обновлено {updated_count} записей")
            return updated_count
        except SQLAlchemyError as e:
            await session.rollback()
            logger.error(f"Ошибка при массовом обновлении: {e}")
            raise
