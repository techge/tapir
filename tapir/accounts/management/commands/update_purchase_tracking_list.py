import csv
import os

from django.core.management import BaseCommand

from tapir import settings
from tapir.accounts.models import TapirUser
from tapir.settings import GROUP_VORSTAND
from tapir.utils.user_utils import UserUtils


class Command(BaseCommand):
    help = "Updates the file containing the list of users that allowed purchase tracking and synchronizes it with the BioOffice server."
    FILE_NAME = "members-current.csv"

    def handle(self, *args, **options):
        self.write_users_to_file()
        self.send_file_to_server()

    @classmethod
    def write_users_to_file(cls):
        with open(cls.FILE_NAME, "w", newline="") as csvfile:
            writer = csv.writer(csvfile, delimiter=";", quoting=csv.QUOTE_MINIMAL)
            writer.writerow(
                [
                    "AdressID",  # Must be exactly 12 characters long and start with a 2. Fill with 0
                    "Nachname",
                    "Vorname",
                    "RabattN",
                    "Strasse",
                    "PLZ",
                    "Ort",
                    "eMail",
                ]
            )

            for user in TapirUser.objects.filter(allows_purchase_tracking=True):
                writer.writerow(
                    [
                        "2" + "{:0>11}".format(user.share_owner.id),
                        user.last_name,
                        user.first_name,
                        18 if user.is_in_group(GROUP_VORSTAND) else 0,
                        UserUtils.get_full_street(user.street, user.street_2),
                        user.postcode,
                        user.city,
                        user.email,
                    ]
                )

    @classmethod
    def send_file_to_server(cls):
        if not settings.DEBUG:
            return

        os.system("mkdir ~/.ssh")
        os.system('echo "$SSH_KEY_PRIVATE" > ~/.ssh/biooffice_id_rsa')
        os.system('echo "$SSH_KEY_PUBLIC" > ~/.ssh/biooffice_id_rsa.pub')
        os.system(
            'echo "$BIOOFFICE_SERVER_SSH_KEY_FINGERPRINT" > ~/.ssh/biooffice_known_hosts'
        )
        os.system(
            f"scp -o 'NumberOfPasswordPrompts=0' -o 'UserKnownHostsFile=~/.ssh/biooffice_known_hosts' -i ~/.ssh/biooffice_id_rsa -P 23 {cls.FILE_NAME} u326634-sub4@u326634.your-storagebox.de:./"
        )
