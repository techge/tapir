from typing import List

from django.utils.translation import gettext_lazy as _

from tapir import settings
from tapir.coop import pdfs
from tapir.coop.models import ShareOwner
from tapir.core.tapir_email_base import TapirEmailBase, all_emails


class ExtraSharesConfirmationEmail(TapirEmailBase):
    num_shares = None
    share_owner = None

    def __init__(self, num_shares: int, share_owner: ShareOwner):
        self.num_shares = num_shares
        self.share_owner = share_owner

    @classmethod
    def get_unique_id(cls) -> str:
        return "tapir.coop.extra_shares_confirmation"

    @classmethod
    def get_name(cls) -> str:
        return _("Extra shares bought")

    @classmethod
    def get_description(cls) -> str:
        return _("Sent when someone who is already a member buys more shares")

    def get_subject_templates(self) -> List:
        return [
            f"coop/email/extra_shares_bought.subject.html",
            f"coop/email/extra_shares_bought.subject.default.html",
        ]

    def get_body_templates(self) -> List:
        return [
            f"coop/email/extra_shares_bought.body.html",
            f"coop/email/extra_shares_bought.body.default.html",
        ]

    def get_extra_context(self) -> dict:
        return {
            "num_shares": self.num_shares,
            "contact_email_address": settings.EMAIL_ADDRESS_MEMBER_OFFICE,
        }

    def get_attachments(self) -> List:
        return [
            (
                "Bestätigung Erwerb Anteile %s.pdf"
                % self.share_owner.get_info().get_display_name(),
                pdfs.get_confirmation_extra_shares_pdf(
                    share_owner=self.share_owner, num_shares=self.num_shares
                ).write_pdf(),
                "application/pdf",
            )
        ]

    @classmethod
    def get_dummy_version(cls) -> TapirEmailBase:
        share_owner = ShareOwner.objects.filter(user__isnull=False).order_by("?")[0]
        mail = cls(num_shares=3)
        mail.get_full_context(
            share_owner=share_owner,
            member_infos=share_owner.get_info(),
            tapir_user=share_owner.user,
        )
        return mail


all_emails[ExtraSharesConfirmationEmail.get_unique_id()] = ExtraSharesConfirmationEmail
