import voluptuous as vol
from homeassistant import config_entries

DOMAIN = "learning_water_purifier"


class LearningWaterPurifierConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Learning Water Purifier."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_POLL

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            if not user_input.get("name", "").strip():
                errors["base"] = "name_required"
            else:
                return self.async_create_entry(
                    title=user_input["name"], data=user_input
                )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required("name", default="Learning Water Purifier"): str,
                }
            ),
            errors=errors,
        )
