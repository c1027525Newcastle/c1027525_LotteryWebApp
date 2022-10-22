# IMPORTS
import logging

from flask import Blueprint, render_template, request, flash

from app import db
from models import User, Draw
from sqlalchemy.orm import make_transient

# CONFIG
lottery_blueprint = Blueprint('lottery', __name__, template_folder='templates')


# VIEWS
# view lottery page
@lottery_blueprint.route('/lottery')
def lottery():
    return render_template('lottery/lottery.html')


@lottery_blueprint.route('/add_draw', methods=['POST'])
def add_draw():
    submitted_draw = ''
    for i in range(6):
        submitted_draw += request.form.get('no' + str(i + 1)) + ' '
    submitted_draw.strip()

    # 3.3 Checking for the user and getting his respective draw_key
    # 3.3 Need  to know how to know what user is logged so gonna need some code
    # 3.3 Until then just keep this line id_user = 1 so we get the admin draw_key
    id_user = 1
    user = User.query.filter_by(id=id_user).first()
    # 3.3 Might want to do an #if user: and do something else if user not in Draw()
    draw_key = user.lottery_draw_key

    # create a new draw with the form data.
    # 3.3 Added the draw_key as one of the parameters
    new_draw = Draw(user_id=1, numbers=submitted_draw, master_draw=False, lottery_round=0, draw_key=draw_key)  # TODO: update user_id [user_id=1 is a placeholder]

    # add the new draw to the database
    db.session.add(new_draw)
    db.session.commit()

    # re-render lottery.page
    flash('Draw %s submitted.' % submitted_draw)
    return lottery()


# view all draws that have not been played
@lottery_blueprint.route('/view_draws', methods=['POST'])
def view_draws():
    # get all draws that have not been played [played=0]
    playable_draws = Draw.query.filter_by(been_played=False).all()  # TODO: filter playable draws for current user

    # if playable draws exist
    if len(playable_draws) != 0:
        # 3.4 COMMENT Same as above need to change this id_user way to a function that gets you the user id and prob
        # an if if it doesn't
        id_user = 1
        user = User.query.filter_by(id=id_user).first()
        draw_key = user.lottery_draw_key
        for playable_draw in playable_draws:
            make_transient(playable_draw)
            playable_draw.view_lottery_draw(draw_key=draw_key)
        #

        # re-render lottery page with playable draws
        return render_template('lottery/lottery.html', playable_draws=playable_draws)
    else:
        flash('No playable draws.')
        return lottery()


# view lottery results
@lottery_blueprint.route('/check_draws', methods=['POST'])
def check_draws():
    # get played draws
    played_draws = Draw.query.filter_by(been_played=True).all()  # TODO: filter played draws for current user

    # if played draws exist
    if len(played_draws) != 0:
        return render_template('lottery/lottery.html', results=played_draws, played=True)

    # if no played draws exist [all draw entries have been played therefore wait for next lottery round]
    else:
        flash("Next round of lottery yet to play. Check you have playable draws.")
        return lottery()


# delete all played draws
@lottery_blueprint.route('/play_again', methods=['POST'])
def play_again():
    Draw.query.filter_by(been_played=True, master_draw=False).delete(synchronize_session=False)
    db.session.commit()

    flash("All played draws deleted.")
    return lottery()


