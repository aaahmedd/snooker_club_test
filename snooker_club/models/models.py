# -*- coding: utf-8 -*-
from openerp import _
from odoo import models, fields, api
import logging
from datetime import datetime
from openerp.exceptions import Warning, ValidationError
import requests

_logger = logging.getLogger(__name__)


class SnookerClub(models.Model):
    """
    General Dashboard For Stats
    """

    _name = 'snooker.club'

    players_check = fields.Boolean('Import Players')
    logs_line = fields.One2many('logs.of.players', 'sync_log_id', string="Logs Of Players ", copy=True)

    def get_players_data(self):
        try:
            players_counter = 0
            if self.players_check:
                data_check = self.env['players.data'].search([])

                url = "http://api.snooker.org/?t=9&e=403"
                payload = {}
                headers = {
                }

                players = requests.request("POST", url, headers=headers, data=payload).json()
                for player in players:
                    odoo_player = self.env['players.data'].search([('player_id', '=', player['ID'])])
                    if not odoo_player:
                        partners = self.env['players.data'].create({
                            'name': player['ShortName'] or player['FirstName'] + ' ' + player['MiddleName'] + ' ' + player['LastName'],
                            'player_id': player['ID'],
                            'country': player['Nationality'],
                            'gender': 'Male' if player['Sex'] == 'M' else 'Female',
                            'date_of_birth': player['Born'],
                            'twitter': player['Twitter'],
                            'picture_link': player['Photo'],
                            'bio_page_link': player['BioPage'],
                        })
                        players_counter += 1
                else:
                    self.env['logs.of.players'].create({
                        'execution_date_time': datetime.now(),
                        'user_id': self.env.user.id,
                        'no_of_players_synced': players_counter,
                        'sync_status': 'Success',
                        'sync_log_id': self.id,
                    })

                # we can update the player data if it is already created but this data is old, so it is not required.

                if not data_check:
                    url_2 = "http://api.snooker.org/?t=8&p=1&s=2015"
                    players = requests.request("POST", url_2, headers=headers, data=payload).json()

                    for player in players:
                        odoo_player_1 = self.env['players.data'].search([('player_id', '=', player['Player1ID'])])
                        odoo_player_2 = self.env['players.data'].search([('player_id', '=', player['Player2ID'])])
                        if odoo_player_1:
                            if player['WinnerID'] == player['Player1ID']:
                                odoo_player_1.no_of_wins += 1
                                odoo_player_2.no_of_losses += 1
                            else:
                                odoo_player_2.no_of_wins += 1
                                odoo_player_1.no_of_losses += 1

                self.env.cr.commit()

        except Exception as e:
            raise ValidationError(e)


class PlayersData(models.Model):
    """
    It Contains the data of players
    """

    _name = 'players.data'

    name = fields.Char(string='Name')
    player_id = fields.Char(string='Player ID')
    country = fields.Char(string='Nationality')
    gender = fields.Char(string='Gender')
    date_of_birth = fields.Char(string='Date Of Birth')
    twitter = fields.Char(string='Twitter')
    picture_link = fields.Char(string='Picture')
    bio_page_link = fields.Char(string='Bio Page')
    no_of_wins = fields.Integer(string='# Of Wins')
    no_of_losses = fields.Integer(string='# Of Losses')

    # @api.model
    # def search_read(self, domain=None, fields=None, offset=0, limit=None, order=None):
    #     self._compute_player_wins()
    #     res = super(PlayersData, self).search_read(domain, fields, offset, limit, order)
    #     return res

    def get_picture(self):
        return {
            'name': 'Go to website',
            'res_model': 'ir.actions.act_url',
            'type': 'ir.actions.act_url',
            'target': 'new',
            'url': self.picture_link
        }

    def get_bio_page(self):
        return {
            'name': 'Go to website',
            'res_model': 'ir.actions.act_url',
            'type': 'ir.actions.act_url',
            'target': 'new',
            'url': self.bio_page_link
        }


class LogsOfPlayers(models.Model):
    _name = 'logs.of.players'

    sync_log_id = fields.Many2one('snooker.club', string='Partner Reference', required=True,
                                  ondelete='cascade', index=True, copy=False)

    execution_date_time = fields.Datetime('Execution Date/Time')
    no_of_players_synced = fields.Integer('# Of Players')
    sync_status = fields.Char(string='Sync Status')
    user_id = fields.Many2one('res.users', 'User')

