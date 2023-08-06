from typing import Mapping, Optional

from vital.api.api import API


class Link(API):
    """Endpoints for managing link tokens."""

    def create(
        self,
        user_id: str,
        provider: Optional[str] = None,
        redirect_url: Optional[str] = None,
    ) -> Mapping[str, str]:
        """
        Create a Link token.
        :param str user_id: user's id returned by service.
        """
        return self.client.post(
            "/link/token",
            {"user_id": user_id, "provider": provider, "redirect_url": redirect_url},
        )

    def password_provider(
        self, link_token: str, provider: str, username: str, password: str
    ) -> Mapping[str, str]:
        """
        Connect a password auth provider.
        :param str link_token: link_token created.
        :param str provider: Provider name.
        :param str username: username.
        :param str password: password.
        """
        return self.client.post(
            f"/link/provider/password/{provider}",
            {"username": username, "password": password},
            headers={"LinkToken": link_token},
        )

    def email_provider(
        self, link_token: str, provider: str, email: str, region: Optional[str] = None
    ) -> Mapping[str, str]:
        """
        Connect a password auth provider.
        :param str link_token: link_token created.
        :param str provider: Provider name.
        :param str username: username.
        :param str password: password.
        """
        return self.client.post(
            f"/link/provider/email/{provider}",
            {"email": email, "region": region},
            headers={"LinkToken": link_token},
        )

    def oauth_provider(
        self,
        link_token: str,
        provider: str,
    ) -> Mapping[str, str]:
        """
        Get link to oAuth provider.
        :param str link_token: link_token created.
        :param str provider: Provider name.
        """
        return self.client.get(
            f"/link/provider/oauth/{provider}",
            headers={"LinkToken": link_token},
        )
