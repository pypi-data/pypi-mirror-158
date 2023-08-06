odoo.define("minecraft_field_tellraw.minecraft_tellraw_field", function (require) {
  "use strict";

  const AbstractFieldOwl = require("web.AbstractFieldOwl");
  const OwlDialog = require("web.OwlDialog");
  const core = require("web.core");

  const _lt = core._lt;

  const {Component} = owl;
  const {useState, useRef} = owl.hooks;

  class MinecraftTellrawHoverEventTextDialog extends Component {
    constructor(...args) {
      super(...args);
      this._newDialogRef = useRef("newDialog");
      // Grepper odoo owl usestate
      this.state = useState({
        customFont: false,
        defaultColor: true,
        value: {},
        previewText: "",
      });
      // End grepper
      if (Object.keys(this.props.editValue).length) {
        this._setEditValue(this.props.editValue, this.props.index);
      }
    }
    patched() {
      this._generatePreviewText();
    }
    onChangeCustomFont(event) {
      this.state.customFont = event.target.checked;
    }
    onChangeDefaultColor(event) {
      this.state.defaultColor = event.target.checked;
    }
    onChangeText(event) {
      const value = event.target.value;
      if (value) {
        this.state.value.text = value;
      } else {
        this.state.value.text = "";
      }
    }
    onChangeColor(event) {
      if (!this.state.defaultColor) {
        const color = event.target.value;
        if (color) {
          this.state.value.color = color;
        }
      }
    }
    onChangeBold(event) {
      this.state.value.bold = event.target.checked;
    }
    onChangeItalic(event) {
      this.state.value.italic = event.target.checked;
    }
    onChangeUnderlined(event) {
      this.state.value.underlined = event.target.checked;
    }
    onChangeStrikethrough(event) {
      this.state.value.strikethrough = event.target.checked;
    }
    onChangeObfuscated(event) {
      this.state.value.obfuscated = event.target.checked;
    }
    onChangeFont(event) {
      if (this.state.customFont) {
        const font = event.target.value;
        if (font) {
          this.state.value.font = font;
        }
      }
    }
    onClickSave() {
      if (this.__owl__.parent.state.fromEdit) {
        this.__owl__.parent.state.values[this.index] = this.state.value;
      } else {
        this.__owl__.parent.state.values.push(this.state.value);
      }
      this.__owl__.parent.state.fromEdit = false;
      this._newDialogRef.comp._close();
    }
    onClickCancel() {
      this._newDialogRef.comp._close();
    }
    _generatePreviewText() {
      const value = this.state.value;
      if (value) {
        if (value.hasOwnProperty("text")) {
          const valueSpan = $("<span />");
          valueSpan.text(value.text);
          if (value.hasOwnProperty("color")) {
            valueSpan.css("color", value.color);
          }
          if (value.hasOwnProperty("bold")) {
            valueSpan.css("font-weight", value.bold ? "bold" : "normal");
          }
          if (value.hasOwnProperty("italic")) {
            valueSpan.css("font-style", value.italic ? "italic" : "normal");
          }
          if (value.hasOwnProperty("underlined")) {
            valueSpan.css("text-decoration", value.underlined ? "underline" : "none");
          }
          if (value.hasOwnProperty("strikethrough")) {
            valueSpan.css(
              "text-decoration",
              value.strikethrough ? "line-through" : valueSpan.css("text-decoration")
            );
          }
          if (
            value.hasOwnProperty("underlined") &&
            value.hasOwnProperty("strikethrough") &&
            value.underlined &&
            value.strikethrough
          ) {
            valueSpan.css("text-decoration", "underline line-through");
          }
          this.state.previewText = valueSpan[0].outerHTML;
        }
      }
    }
    _setEditValue(value, index) {
      this.index = index;
      this.state.value = Object.assign({}, value);
    }
  }

  Object.assign(MinecraftTellrawHoverEventTextDialog, {
    components: {
      Dialog: OwlDialog,
    },
    editValue: Object,
    template: "MinecraftTellrawHoverEventTextDialog",
  });

  class MinecraftTellrawDialog extends Component {
    constructor(...args) {
      super(...args);
      this.state = useState({
        clickEvent: false,
        hoverEvent: false,
        customFont: false,
        defaultColor: true,
        minecraftTellrawHoverEventTextDialog: false,
        value: {},
        values: [""],
        text: "",
        previewText: "",
        editValue: {},
        fromEdit: false,
        index: 0,
      });
      this._dialogRef = useRef("dialog");
    }
    mounted() {
      if (Object.keys(this.props.editValue).length) {
        this._setEditValue(this.props.editValue);
      }
    }
    patched() {
      this._generatePreviewText();
      this._generateText();
      this._reInitDropdown();
      $("table tbody").sortable({
        handle: "span.o_row_handle",
        cancel: "",
        start: (e, ui) => {
          $(this).attr("data-previndex", ui.item.index());
        },
        update: (e, ui) => {
          const oldIndex = $(this).attr("data-previndex");
          const newIndex = ui.item.index();
          $(this).removeAttr("data-previndex");
          this._updateIndex(oldIndex + 1, newIndex + 1);
        },
      });
    }
    onChangeClickEvent(event) {
      const value = event.target.value;
      if (value && value !== "none") {
        this.state.clickEvent = value;
      } else {
        this.state.clickEvent = false;
      }
    }
    onChangeHoverEvent(event) {
      const value = event.target.value;
      if (value && value !== "none") {
        this.state.hoverEvent = value;
      } else {
        this.state.hoverEvent = false;
      }
    }
    onChangeCustomFont(event) {
      this.state.customFont = event.target.checked;
    }
    onChangeDefaultColor(event) {
      this.state.defaultColor = event.target.checked;
    }
    onChangeText(event) {
      const value = event.target.value;
      if (value) {
        this.state.value.text = value;
      } else {
        this.state.value.text = "";
      }
    }
    onChangeColor(event) {
      if (!this.state.defaultColor) {
        const color = event.target.value;
        if (color) {
          this.state.value.color = color;
        }
      }
    }
    onChangeBold(event) {
      this.state.value.bold = event.target.checked;
    }
    onChangeItalic(event) {
      this.state.value.italic = event.target.checked;
    }
    onChangeUnderlined(event) {
      this.state.value.underlined = event.target.checked;
    }
    onChangeStrikethrough(event) {
      this.state.value.strikethrough = event.target.checked;
    }
    onChangeObfuscated(event) {
      this.state.value.obfuscated = event.target.checked;
    }
    onChangeFont(event) {
      if (this.state.customFont) {
        const font = event.target.value;
        if (font) {
          this.state.value.font = font;
        }
      }
    }
    onChangeClickEventValue(event) {
      const clickEvent = this.state.clickEvent;
      if (clickEvent && clickEvent !== "none") {
        this.state.value.clickEvent = {
          action: clickEvent,
          value: event.target.value,
        };
      }
    }
    onChangeHoverEventValue(event) {
      const hoverEvent = this.state.hoverEvent;
      if (hoverEvent && hoverEvent !== "none") {
        this.state.value.hoverEvent = {
          action: hoverEvent,
          value: event.target.value,
        };
      }
    }
    onClickSave() {
      if (this.state.hoverEvent === "show_text") {
        this.state.value.hoverEvent = {
          action: this.state.hoverEvent,
          value: this.state.values,
        };
      }
      if (!this.__owl__.parent.state.fromEdit) {
        this.__owl__.parent.state.values.push(this.state.value);
      }
      this.__owl__.parent.state.fromEdit = false;
      this.__owl__.parent.state.minecraftTellrawTextDialog = false;
    }
    onClickCancel() {
      this.__owl__.parent.state.minecraftTellrawTextDialog = false;
    }
    onClickRemoveText(index) {
      this.state.values.splice(index, 1);
    }
    onClickEditText(index) {
      this.state.fromEdit = true;
      this.state.editValue = this.state.values[index];
      this.state.index = index;
      this.state.minecraftTellrawHoverEventTextDialog = true;
    }
    openText() {
      this.state.minecraftTellrawHoverEventTextDialog = true;
    }
    openLineBreak() {
      this.state.values.push("\n");
    }
    onDialogClosed() {
      this.state.editValue = {};
      this.state.minecraftTellrawHoverEventTextDialog = false;
    }
    _reInitDropdown() {
      $(document).ready(function () {
        $(".dropdown-toggle").dropdown();
      });
    }
    _generatePreviewText() {
      const value = this.state.value;
      if (value) {
        if (value.hasOwnProperty("text")) {
          const valueSpan = $("<span />");
          valueSpan.text(value.text);
          if (value.hasOwnProperty("color")) {
            valueSpan.css("color", value.color);
          }
          if (value.hasOwnProperty("bold")) {
            valueSpan.css("font-weight", value.bold ? "bold" : "normal");
          }
          if (value.hasOwnProperty("italic")) {
            valueSpan.css("font-style", value.italic ? "italic" : "normal");
          }
          if (value.hasOwnProperty("underlined")) {
            valueSpan.css("text-decoration", value.underlined ? "underline" : "none");
          }
          if (value.hasOwnProperty("strikethrough")) {
            valueSpan.css(
              "text-decoration",
              value.strikethrough ? "line-through" : valueSpan.css("text-decoration")
            );
          }
          if (
            value.hasOwnProperty("underlined") &&
            value.hasOwnProperty("strikethrough") &&
            value.underlined &&
            value.strikethrough
          ) {
            valueSpan.css("text-decoration", "underline line-through");
          }
          this.state.previewText = valueSpan[0].outerHTML;
        }
      }
    }
    _generateText() {
      this.state.text = this.state.values
        .map((value) => {
          if (value.hasOwnProperty("text")) {
            const valueSpan = $("<span />");
            valueSpan.text(value.text);
            if (value.hasOwnProperty("color")) {
              valueSpan.css("color", value.color);
            }
            if (value.hasOwnProperty("bold")) {
              valueSpan.css("font-weight", value.bold ? "bold" : "normal");
            }
            if (value.hasOwnProperty("italic")) {
              valueSpan.css("font-style", value.italic ? "italic" : "normal");
            }
            if (value.hasOwnProperty("underlined")) {
              valueSpan.css("text-decoration", value.underlined ? "underline" : "none");
            }
            if (value.hasOwnProperty("strikethrough")) {
              valueSpan.css(
                "text-decoration",
                value.strikethrough ? "line-through" : "none"
              );
            }
            if (
              value.hasOwnProperty("underlined") &&
              value.hasOwnProperty("strikethrough")
            ) {
              valueSpan.css("text-decoration", "underline line-through");
            }
            return valueSpan[0].outerHTML;
          }
          return value;
        })
        .join("");
    }
    _setEditValue(value) {
      this.state.value = value;
      if (value.hasOwnProperty("hoverEvent")) {
        this.state.hoverEvent = value.hoverEvent.action;
        if (value.hoverEvent.action === "show_text") {
          this.state.values = value.hoverEvent.value;
        }
      }
      if (value.hasOwnProperty("clickEvent")) {
        this.state.clickEvent = value.clickEvent.action;
      }
      this.__owl__.parent.state.editValue = {};
    }
    _updateIndex(oldIndex, newIndex) {
      const values = this.state.values;
      const value = values[oldIndex];
      values.splice(oldIndex, 1);
      values.splice(newIndex, 0, value);
      this.state.values = values;
      // Close dialog because the index changed and the old index is no longer valid
      // should be solved by a better solution
      this.onClickSave();
    }
  }

  Object.assign(MinecraftTellrawDialog, {
    components: {
      Dialog: OwlDialog,
      MinecraftTellrawHoverEventTextDialog,
    },
    editValue: Object,
    template: "FieldMinecraftTellrawText",
  });

  class MinecraftTellrawField extends AbstractFieldOwl {
    constructor(...args) {
      super(...args);
      this.state = useState({
        minecraftTellrawTextDialog: false,
        values: [""],
        text: "",
        editValue: {},
        fromEdit: false,
      });
      if (this.value.values) {
        this.state.values = this.value.values;
        this._generateText();
      }
      this.lastValue = undefined;
    }
    mounted() {
      $(this.el)
        .find("table tbody.dropdown-values")
        .sortable({
          handle: "span.o_row_handle",
          cancel: "",
          start: (e, ui) => {
            $(this).attr("data-previndex", ui.item.index());
          },
          update: (e, ui) => {
            const oldIndex = $(this).attr("data-previndex");
            const newIndex = ui.item.index();
            $(this).removeAttr("data-previndex");
            this._updateIndex(oldIndex + 1, newIndex + 1);
          },
        });
    }
    patched() {
      this._generateText();
      const val = {values: this.state.values};
      // Grepper js compare objects
      const isEqual = (...objects) =>
        objects.every((obj) => JSON.stringify(obj) === JSON.stringify(objects[0]));
      if (!isEqual(this.lastValue, val)) {
        // End grepper
        // grepper odoo field set value
        this._setValue(val);
        // End grepper
        this.lastValue = val;
      }
    }
    onClickRemoveText(index) {
      // Grepper js remove item on index
      this.state.values.splice(index, 1);
      // End grepper
    }
    onClickEditText(index) {
      this.state.fromEdit = true;
      this.state.editValue = this.state.values[index];
      this.state.minecraftTellrawTextDialog = true;
    }
    openText() {
      this.state.minecraftTellrawTextDialog = true;
    }
    openLineBreak() {
      this.state.values.push("\n");
    }
    // Buggy if you want to close the dialog if you opened a second one before
    onDialogClosed() {
      this.state.minecraftTellrawTextDialog = false;
    }
    _setValue(value, options) {
      // We try to avoid doing useless work, if the value given has not changed.
      if (this._isLastSetValue(value)) {
        return Promise.resolve();
      }
      this._lastSetValue = value;
      this._isValid = true;
      if (!(options && options.forceChange) && this._isSameValue(value)) {
        return Promise.resolve();
      }
      return new Promise((resolve, reject) => {
        const changes = {};
        changes[this.name] = value;
        this.trigger("field-changed", {
          dataPointID: this.dataPointId,
          changes: changes,
          viewType: this.viewType,
          doNotSetDirty: options && options.doNotSetDirty,
          notifyChange: !options || options.notifyChange !== false,
          allowWarning: options && options.allowWarning,
          onSuccess: resolve,
          onFailure: reject,
        });
      });
    }
    _generateText() {
      this.state.text = this.state.values
        .map((value) => {
          if (value.hasOwnProperty("text")) {
            const valueSpan = $("<span />");
            valueSpan.text(value.text);
            if (value.hasOwnProperty("color")) {
              valueSpan.css("color", value.color);
            }
            if (value.hasOwnProperty("bold")) {
              valueSpan.css("font-weight", value.bold ? "bold" : "normal");
            }
            if (value.hasOwnProperty("italic")) {
              valueSpan.css("font-style", value.italic ? "italic" : "normal");
            }
            if (value.hasOwnProperty("underlined")) {
              valueSpan.css("text-decoration", value.underlined ? "underline" : "none");
            }
            if (value.hasOwnProperty("strikethrough")) {
              valueSpan.css(
                "text-decoration",
                value.strikethrough ? "line-through" : "none"
              );
            }
            if (
              value.hasOwnProperty("underlined") &&
              value.hasOwnProperty("strikethrough")
            ) {
              valueSpan.css("text-decoration", "underline line-through");
            }
            return valueSpan[0].outerHTML;
          }
          return value;
        })
        .join("");
    }
    _updateIndex(oldIndex, newIndex) {
      const values = this.state.values;
      const value = values[oldIndex];
      values.splice(oldIndex, 1);
      values.splice(newIndex, 0, value);
      this.state.values = values;
      // Grepper odoo js reload widget
      this.trigger("reload");
      // End grepper
    }
  }

  Object.assign(MinecraftTellrawField, {
    components: {
      MinecraftTellrawDialog,
    },
    template: "FieldMinecraftTellraw",
    supportedFieldTypes: ["serialized"],
    description: _lt("Minecraft Tellraw Field"),
  });

  return {
    MinecraftTellrawField: MinecraftTellrawField,
    MinecraftTellrawDialog: MinecraftTellrawDialog,
    MinecraftTellrawHoverEventTextDialog: MinecraftTellrawHoverEventTextDialog,
  };
});
