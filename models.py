from bootstrap import db, app
from random import choice
from math import floor
from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


# a project can have multiple cards and multiple items
class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    items = relationship('Item', back_populates='project')
    cards = relationship('Card', back_populates='project')

    def __repr__(self):
        return str(self)

    def __str__(self):
        return f'{self.__class__.__name__}: {self.name}'


# an item is a single string that can show up on a card
class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    detail = db.Column(db.String(80), nullable=False)
    free_space = db.Column(db.Boolean, nullable=False, default=False)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    project = relationship('Project', back_populates='items')

    def __repr__(self):
        return str(self)

    def __str__(self):
        return f'{self.__class__.__name__}({self.id}): {self.detail}'


# a card is a unique combination of items
class Card(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    rows = db.Column(db.Integer, nullable=False)
    cols = db.Column(db.Integer, nullable=False)
    card_items = relationship('CardItem', back_populates='card')
    project = relationship('Project', back_populates='cards')

    def __repr__(self):
        return str(self)

    def __str__(self):
        return f'{self.__class__.__name__}: {self.id} ({self.rows} x {self.cols})'

    @classmethod
    def generate(cls, project_id, rows, cols):
        card = cls()
        card.project_id = project_id
        card.rows = rows
        card.cols = cols
        db.session.add(card)
        db.session.commit()

        # now generate all the items on this card
        all_items = Item.query.filter_by(project_id=project_id, free_space=False).all()
        free_spaces = Item.query.filter_by(project_id=project_id, free_space=True).all()
        items = []
        if (rows == cols) and (rows % 2 == 1) and free_spaces:
            free_space = int((rows - 1) / 2)
        else:
            free_space = False

        for i in range(0, rows * cols):
            ci = CardItem()
            ci.card_id = card.id
            ci.row = i % rows
            ci.col = floor(i/cols)
            if free_space and ci.row == ci.col and ci.row == free_space:
                selection = choice(free_spaces)
                free_spaces.remove(selection)
            else:
                selection = choice(all_items)
                all_items.remove(selection)
            ci.item_id = selection.id
            items.append(ci)
        db.session.add_all(items)
        db.session.commit()
        return card

    @classmethod
    def random(cls, project_id):
        return cls.query.filter_by(project_id=project_id).order_by(func.random()).limit(1).one()


class CardItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    card_id = db.Column(db.Integer, db.ForeignKey('card.id'), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False)
    row = db.Column(db.Integer, nullable=False)
    col = db.Column(db.Integer, nullable=False)
    card = relationship('Card', back_populates='card_items')
    item = relationship('Item')
    __table_args__ = (
        UniqueConstraint('card_id', 'item_id', name='_card_item_uc'),         # can only add an item once to a card
        UniqueConstraint('card_id', 'row', 'col', name='_card_position_uc'),  # can only put one item in a position
    )

    def __repr__(self):
        return str(self)

    def __str__(self):
        return f'{self.__class__.__name__}: {self.card_id} ({self.row},{self.col})'

    def __lt__(self, other):
        # ordering for 2x2 should be (0,0),(0,1),(1,0),(1,1)
        return self.card.rows * self.row + self.col < other.card.rows * other.row + other.col


db.create_all(app=app)
