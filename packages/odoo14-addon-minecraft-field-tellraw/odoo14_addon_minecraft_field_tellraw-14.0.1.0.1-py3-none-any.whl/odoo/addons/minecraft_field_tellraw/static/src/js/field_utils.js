odoo.define("minecraft_field_tellraw.field_utils", function (require) {
  "use strict";

  require("web.field_utils").format.serialized = function (value) {
    return JSON.stringify(value);
  };
  require("web.field_utils").parse.serialized = function (value) {
    return JSON.stringify(value);
  };
});
