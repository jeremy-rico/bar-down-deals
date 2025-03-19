from datetime import datetime, timedelta, timezone

from sqlalchemy import delete, select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import col, func

from src.core.exceptions import AlreadyExistsException, NotFoundException
from src.deals.models import Deal
from src.products.models import Category, CategoryProductLink, Product


class DealRepository:
    """Repository for handling Hero database operations."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(
        self,
        sort: str,
        order: str,
        page: int,
        limit: int,
        added_since: str,
        categories: list[int] | None,
    ) -> list[Deal]:
        """Get filtered deals.

        Returns:
            List[Deal]: List of all deals
        """
        stmt = select(Deal)

        if categories:
            stmt = stmt.join(Product).join(CategoryProductLink)
            stmt = (
                stmt.where(col(CategoryProductLink.category_id).in_(categories))
                .group_by(col(Deal.id))
                .having(
                    func.count(col(CategoryProductLink.category_id).distinct())
                    >= len(categories)
                )
            )

        if added_since:
            timeframes = {
                "today": datetime.now(timezone.utc) - timedelta(days=1),
                "week": datetime.now(timezone.utc) - timedelta(weeks=1),
                "month": datetime.now(timezone.utc) - timedelta(weeks=4),
                "year": datetime.now(timezone.utc) - timedelta(days=365),
            }
            if added_since in timeframes:
                stmt = stmt.filter(col(Deal.created_at) >= timeframes[added_since])

        # TODO: sort by best
        if sort == "date" and order == "asc":
            stmt = stmt.order_by(col(Deal.created_at).asc())
        elif sort == "date" and order == "desc":
            stmt = stmt.order_by(col(Deal.created_at).desc())
        elif sort == "discount" or sort == "best":
            stmt = stmt.order_by(col(Deal.discount).desc())
        elif sort == "price" and order == "asc":
            stmt = stmt.order_by(col(Deal.price).asc())
        elif sort == "price" and order == "desc":
            stmt = stmt.order_by(col(Deal.price).desc())
        elif sort == "alphabetical":
            stmt = stmt.order_by(col(Deal.Product.name).desc())

        offset = (page - 1) * limit
        stmt = stmt.offset(offset).limit(limit)
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    # async def create(self, deal_data: DealCreate) -> Deal:
    #     """Create a new deal.
    #
    #     Args:
    #         deal_data: Deal creation data
    #
    #     Returns:
    #         Deal: Created deal
    #
    #     Raises:
    #         AlreadyExistsException: If deal with same alias already exists
    #     """
    #     deal = Deal(**deal_data.model_dump())
    #     try:
    #         self.session.add(deal)
    #         await self.session.commit()
    #         await self.session.refresh(deal)
    #         return deal
    #     except IntegrityError:
    #         await self.session.rollback()
    #         raise AlreadyExistsException(
    #             f"Deal with alias {deal_data.id} already exists"
    #         )
    #
    async def get_by_id(self, deal_id: int) -> Deal:
        """Get deal by ID.

        Args:
            deal_id: Deal ID

        Returns:
            Deal: Found deal

        Raises:
            NotFoundException: If deal not found
        """
        stmt = select(Deal).where(col(Deal.id) == deal_id)
        result = await self.session.execute(stmt)
        deal = result.scalar_one_or_none()
        # deal = result.scalar.first()

        if not deal:
            raise NotFoundException(f"Deal with id {deal_id} not found")
        return deal

    # async def update(self, deal_id: int, deal_data: DealUpdate) -> Deal:
    #     """Update deal by ID.
    #
    #     Args:
    #         deal_id: Deal ID
    #         deal_data: Deal update data
    #
    #     Returns:
    #         Deal: Updated deal
    #
    #     Raises:
    #         NotFoundException: If deal not found
    #     """
    #     update_data = deal_data.model_dump(exclude_unset=True)
    #     if not update_data:
    #         raise ValueError("No fields to update")
    #
    #     query = update(Deal).where(Deal.id == deal_id).values(**update_data)
    #     result = await self.session.execute(query)
    #
    #     if result.rowcount == 0:
    #         raise NotFoundException(f"Deal with id {deal_id} not found")
    #
    #     await self.session.commit()
    #     return await self.get_by_id(deal_id)
    #
    # async def delete(self, deal_id: int) -> None:
    #     """Delete deal by ID.
    #
    #     Args:
    #         deal_id: Deal ID
    #
    #     Raises:
    #         NotFoundException: If deal not found
    #     """
    #     query = delete(Deal).where(Deal.id == deal_id)
    #     result = await self.session.execute(query)
    #
    #     if result.rowcount == 0:
    #         raise NotFoundException(f"Deal with id {deal_id} not found")
    #


# class HeroRepository:
#     """Repository for handling Hero database operations."""
#
#     def __init__(self, session: AsyncSession):
#         self.session = session
#
#     async def create(self, hero_data: HeroCreate) -> Hero:
#         """Create a new hero.
#
#         Args:
#             hero_data: Hero creation data
#
#         Returns:
#             Hero: Created hero
#
#         Raises:
#             AlreadyExistsException: If hero with same alias already exists
#         """
#         hero = Hero(**hero_data.model_dump())
#         try:
#             self.session.add(hero)
#             await self.session.commit()
#             await self.session.refresh(hero)
#             return hero
#         except IntegrityError:
#             await self.session.rollback()
#             raise AlreadyExistsException(
#                 f"Hero with alias {hero_data.alias} already exists"
#             )
#
#     async def get_by_id(self, hero_id: int) -> Hero:
#         """Get hero by ID.
#
#         Args:
#             hero_id: Hero ID
#
#         Returns:
#             Hero: Found hero
#
#         Raises:
#             NotFoundException: If hero not found
#         """
#         query = select(Hero).where(Hero.id == hero_id)
#         result = await self.session.execute(query)
#         hero = result.scalar_one_or_none()
#
#         if not hero:
#             raise NotFoundException(f"Hero with id {hero_id} not found")
#         return hero
#
#     async def get_all(self) -> list[Hero]:
#         """Get all heroes.
#
#         Returns:
#             List[Hero]: List of all heroes
#         """
#         query = select(Hero)
#         result = await self.session.execute(query)
#         return list(result.scalars().all())
#
#     async def update(self, hero_id: int, hero_data: HeroUpdate) -> Hero:
#         """Update hero by ID.
#
#         Args:
#             hero_id: Hero ID
#             hero_data: Hero update data
#
#         Returns:
#             Hero: Updated hero
#
#         Raises:
#             NotFoundException: If hero not found
#         """
#         update_data = hero_data.model_dump(exclude_unset=True)
#         if not update_data:
#             raise ValueError("No fields to update")
#
#         query = update(Hero).where(Hero.id == hero_id).values(**update_data)
#         result = await self.session.execute(query)
#
#         if result.rowcount == 0:
#             raise NotFoundException(f"Hero with id {hero_id} not found")
#
#         await self.session.commit()
#         return await self.get_by_id(hero_id)
#
#     async def delete(self, hero_id: int) -> None:
#         """Delete hero by ID.
#
#         Args:
#             hero_id: Hero ID
#
#         Raises:
#             NotFoundException: If hero not found
#         """
#         query = delete(Hero).where(Hero.id == hero_id)
#         result = await self.session.execute(query)
#
#         if result.rowcount == 0:
#             raise NotFoundException(f"Hero with id {hero_id} not found")
#
#         await self.session.commit()
