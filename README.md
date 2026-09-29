# EHEIM Digital LEDcontrol+ for Home Assistant

An experimental HACS custom integration for EHEIM LEDcontrol+ controllers that
report device `version: 3`. It embeds the required EHEIM client library, so it
does not depend on an unreleased upstream library version.

## Status

This release includes an anonymized fixture from an LEDcontrol+ with:

- `tankconfig`: `["FRESH_PLANTS"]`
- `power`: `["34"]`
- CCV values: `[98, 98, 98]`

The bundled controller test verifies that this format is detected as
`version: 3` and exposes one configured channel. The integration creates
entities only for configured channels; the example above therefore creates one
light entity.

This project is an interim solution until the corresponding support is merged
into the official `eheimdigital` library and Home Assistant integration.

## Upstream tracking

The LEDcontrol+ (`version: 3`) work is being tracked upstream:

- [Home Assistant Core issue #160502](https://github.com/home-assistant/core/issues/160502)
  documents the reported device format and the missing support.
- [Home Assistant Core PR #177948](https://github.com/home-assistant/core/pull/177948)
  is the current broader EHEIM Digital integration refactor.
- [eheimdigital Codeberg PR #8](https://codeberg.org/autinerd/eheimdigital/pulls/8)
  contains the initial library-side LEDcontrol+ implementation.

This custom integration carries the required library and integration changes
while those upstream contributions are reviewed and released.

## Installation

1. Install [HACS](https://hacs.xyz/) if it is not installed already.
2. In **HACS > Integrations**, open the menu and select **Custom repositories**.
3. Add `https://github.com/jowi24/ha-eheimdigital-ledcontrol` as an
   **Integration** repository.
4. Install **EHEIM Digital LEDcontrol+**.
5. Restart Home Assistant.
6. Add **EHEIM Digital LEDcontrol+** through
   **Settings > Devices & services > Add integration**.

The integration can coexist with Home Assistant's built-in EHEIM Digital
integration because it uses the separate domain `eheimdigital_ledcontrol`.
Do not configure both integrations against the same EHEIM hub at the same
time: each maintains its own WebSocket connection.

## Updating and returning to official support

HACS manages future releases. When official LEDcontrol+ support is available:

1. Remove this custom integration.
2. Restart Home Assistant.
3. Add or reconfigure the built-in **EHEIM Digital** integration.

The custom integration intentionally has separate entity IDs and does not
migrate its config entry into the built-in integration.

## Development

The client library is vendored in
`custom_components/eheimdigital_ledcontrol/lib/`. It is based on
`eheimdigital` 1.7.1 plus LEDcontrol+ (`version: 3`) support.

The next upstream change, once the corresponding library support is accepted
and released, is a Home Assistant Core PR that implements the same dynamic
channel handling without the vendored library.
