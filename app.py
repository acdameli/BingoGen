from bootstrap import db, app
from enum import Enum
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from models import Project, Card, Item


class CardFormat(Enum):
    HTML = 'html'
    PDF = 'pdf'
    JPEG = 'jpeg'
    PNG = 'png'


@app.route('/')
def hello_world():
    return 'BINGO CARDS!'


@app.route('/projects/')
def project_index():
    return render_template('projects/index.html', projects=Project.query.all())


@app.route('/projects/', methods=['POST'])
@app.route('/projects/<int:project_id>', methods=['POST'])
def project_create(project_id: int = None):
    name = request.form.get('name')
    project = Project.query.filter_by(id=project_id) if project_id else Project()
    project.name = name
    db.session.add(project)
    db.session.commit()
    return redirect(url_for('project_get', project_id=project.id))


@app.route('/projects/<int:project_id>')
def project_get(project_id: int):
    project = Project.query.filter_by(id=project_id).one()
    return render_template('projects/get.html', project=project)


@app.route('/projects/<int:project_id>/items', methods=['POST'])
def item_create(project_id: int):
    i = Item()
    i.project_id = project_id
    i.detail = request.form.get('detail')
    if not i.detail:
        return 'You failed to provide a string for this item'
    i.free_space = bool(request.form.get('free_space', False))
    db.session.add(i)
    db.session.commit()
    return redirect(url_for('project_get', project_id=project_id))


@app.route('/projects/<int:project_id>/cards')
def card_index(project_id: int):
    project = Project.query.filter_by(id=project_id).one()
    return render_template('cards/index.html', project=project)


@app.route('/projects/<int:project_id>/cards/generate', methods=['POST'])
@app.route('/projects/<int:project_id>/cards/generate/<int:rows>', methods=['GET'])
def card_generate(project_id: int, rows: int = None):
    rows = int(request.form.get('rows') if request.method == 'POST' else rows)
    card = Card.generate(project_id, rows, rows)  # always generate square cards
    return redirect(url_for('card_get', project_id=project_id, card_id=card.id))


@app.route('/projects/<int:project_id>/cards/random')
@app.route('/projects/<int:project_id>/cards/<int:card_id>')
def card_get(project_id: int, card_id: int = None):
    card_format = str(request.args.get('format', default=CardFormat.HTML.name)).upper()
    if card_id:
        card = Card.query.filter_by(project_id=project_id, id=card_id).one()
    else:
        # select a random card
        num_cards = Card.query.filter_by(project_id=project_id).count()
        if not num_cards:
            return 'No cards exist for this project'

        card = Card.random(project_id)

    if card_format not in CardFormat.__members__:
        return f'Invalid format requested "{card_format}" must be one of: {CardFormat.__members__}'
    elif card_format.upper() == CardFormat.HTML.name:
        return render_template('cards/get.html', card=card)
    else:
        return f'Not yet implemented {card_format} != {CardFormat.HTML}'


@app.route('/projects/<int:project_id>/items')
def item_index(project_id: int):
    return str(Item.query.filter_by(project_id=project_id).all())


if __name__ == '__main__':
    app.run(debug=True)
