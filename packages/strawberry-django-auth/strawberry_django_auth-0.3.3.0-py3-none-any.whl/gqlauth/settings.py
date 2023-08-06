import logging
import warnings

from django.conf import settings as django_settings
from django.test.signals import setting_changed

from gqlauth.settings_type import DjangoSetting, GqlAuthSettings

logger = logging.getLogger(__name__)

gqlauth_settings: GqlAuthSettings = None

if user_settings := getattr(django_settings, "GQL_AUTH", False):
    if isinstance(user_settings, GqlAuthSettings):
        gqlauth_settings = user_settings

    else:
        raise Exception(
            f"GQL_AUTH settings should be of type "
            f"{GqlAuthSettings}, but you provided {type(user_settings)}"
        )

else:
    logger.warning(
        "GQL AUTH: You have not provided" "any custom gql auth settings falling back to defaults"
    )
    gqlauth_settings = GqlAuthSettings()

defaults = GqlAuthSettings()
# retain django_settings
for name, setting in gqlauth_settings.__dataclass_fields__.items():
    value = getattr(gqlauth_settings, name)
    if setting.type is DjangoSetting and value is getattr(defaults, name):
        setattr(gqlauth_settings, name, value())
del defaults


# should be deprecated probably
def reload_gqlauth_settings(*args, **kwargs):
    global gqlauth_settings
    setting, value = kwargs["setting"], kwargs["value"]
    if setting == "GQL_AUTH" and isinstance(value, dict):
        gqlauth_settings = GqlAuthSettings(**value)
    else:
        warnings.warn(
            f"reload_gqlauth_settings" f"should be called with a dict, not {str(type(value))}"
        )


setting_changed.connect(reload_gqlauth_settings)
