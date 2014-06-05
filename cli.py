import os
import click

import models
from views import panic_json
from trellis import Trellis


class ApplicationContext(object):
    def __init__(trellis):
        self.trellis = trellis

# Pass context thing


@click.group()
@click.argument('--board', help="The board ID to use")
@click.option('--get-token', is_flag=True, help="Get token for Trello.")
@click.option('--token', help="Trello token.")
def cli(board, get_token, token):
    """ This is a command line app to get useful stats from a trello board
        and report on them in useful ways.

        Requires the following environment varilables:

        TRELLIS_APP_KEY=<your key here>
        TRELLIS_APP_TOKEN=<your token here>
    """
    models.Snapshots.create_table(fail_silently=True)
    trellis = Trellis(os.environ.get('TRELLIS_APP_KEY'),
                      os.environ.get('TRELLIS_APP_TOKEN'), board)
    click.echo(trellis)


@click.command()
@click.option('--board', help='Board ID of board to look at.')
@click.option('--cycle-time', is_flag=True, help='Include cycle time in report')
@click.option('--spend', is_flag=True, help='Include spend in report')
@click.option('--revenue', is_flag=True, help='Include revenue in report')
@click.option('--out', type=click.File, help='File to write report out to.')
def report(board, cycle_time, spend, revenue, template, out):
    """
       Reporting mode: - Send templated reports with graphs, or output to json
        -> trellis report --board=87hiudhw
                          --cycle-time
                          --spend="340,654"
                          --revenue="456,435"
                          --template=templates/client.html
                          --out=report.html
    """
    if board:
        click.echo(trellis.print_lists_in_board(board))
        exit()


@click.command()
@click.option('--board', help='Board ID of board to look at.')
@click.option('--cycle-time', is_flag=True, help='Include cycle time in report')
@click.option('--spend', is_flag=True, help='Include spend in report')
@click.option('--revenue', is_flag=True, help='Include revenue in report')
@click.option('--done', help='Title of column which represents Done.')
def snapshot(board, cycle_time, spend, revenue, done):
    """
        Recording mode - Daily snapshots of a board for ongoing reporting:
         -> trellis report --board=87hiudhw
                          --cycle-time
                          --spend
                          --revenue
                          --done=Done

    """

    trellis = Trellis(board_id=board)
    if board:
        print trellis.print_lists_in_board(board)
        exit()

    else:
        cards = trellis.get_list_data(done)
        ct = trellis.cycle_time(cards)
        print ct
        # if save:
        #     models.CycleTime.create(list_id=done, cycle_time=ct)

        if output:
            panic_json(output)

cli.add_command(snapshot)
cli.add_command(report)

if __name__ == '__main__':
    cli()
