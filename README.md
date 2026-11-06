# Granular Field Permissions

<!--
Developer Note - Remove Me!

The README will have certain links/images broken until the PR is merged into `develop`. Update the GitHub links with whichever branch you're using (main etc.) if different.

The logo of the project is a placeholder (docs/images/icon-granular-field-permissions.png) - please replace it with your app icon, making sure it's at least 200x200px and has a transparent background!

To avoid extra work and temporary links, make sure that publishing docs (or merging a PR) is done at the same time as setting up the docs site on RTD, then test everything.
-->

<p align="center">
  <img src="https://raw.githubusercontent.com/nautobot/nautobot-app-granular-field-permissions/develop/docs/images/icon-granular-field-permissions.png" class="logo" height="200px">
  <br>
  <a href="https://github.com/nautobot/nautobot-app-granular-field-permissions/actions"><img src="https://github.com/nautobot/nautobot-app-granular-field-permissions/actions/workflows/ci.yml/badge.svg?branch=main"></a>
  <a href="https://docs.nautobot.com/projects/granular-field-permissions/en/latest/"><img src="https://readthedocs.org/projects/nautobot-app-granular-field-permissions/badge/"></a>
  <a href="https://pypi.org/project/granular-field-permissions/"><img src="https://img.shields.io/pypi/v/granular-field-permissions"></a>
  <a href="https://pypi.org/project/granular-field-permissions/"><img src="https://img.shields.io/pypi/dm/granular-field-permissions"></a>
  <br>
  An <a href="https://networktocode.com/nautobot-apps/">App</a> for <a href="https://nautobot.com/">Nautobot</a>.
</p>

## Overview

This app allows to "lock" certain fields out of certain models.
Once a model has locked fields, you need an additional permission to edit them.

Using nautobot's custom permission model, users need to be assigned a field_<fieldname> or custom_field_<cfname> to edit them.

Superadmins have all privileges implicitly so are always allowed to do anything