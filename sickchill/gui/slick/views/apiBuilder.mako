<%!
    import json
    from urllib.parse import urljoin

    from sickchill import settings
%>
<!DOCTYPE html>
<html>
    <head>
        <meta charset="utf-8">
        <meta name="robots" content="noindex, nofollow">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=0">

        <% themeColors = { "dark": "#15528F", "light": "#333333" } %>
        <!-- Android -->
        <meta name="theme-color" content="${themeColors[settings.THEME_NAME]}">
        <!-- Windows Phone -->
        <meta name="msapplication-navbutton-color" content="${themeColors[settings.THEME_NAME]}">
        <!-- iOS -->
        <meta name="apple-mobile-web-app-status-bar-style" content="${themeColors[settings.THEME_NAME]}">

        <title>SickChill - ${title}</title>

        <!--[if lt IE 9]>
            <script src="${static_url('js/html5shiv.min.js')}"></script>
            <script src="${static_url('js/respond.min.js')}"></script>
        <![endif]-->

        <meta name="msapplication-TileColor" content="#FFFFFF">
        <meta name="msapplication-TileImage" content="${static_url('images/ico/favicon-144.png')}">
        <meta name="msapplication-config" content="${static_url('css/browserconfig.xml')}">

        <meta data-var="scRoot" data-content="${scRoot}">
        <meta data-var="themeSpinner" data-content="${('', '-dark')[settings.THEME_NAME == 'dark']}">
        <meta data-var="anonURL" data-content="${settings.ANON_REDIRECT}">

        <meta data-var="settings.ANIME_SPLIT_HOME" data-content="${settings.ANIME_SPLIT_HOME}">
        <meta data-var="settings.ANIME_SPLIT_HOME_IN_TABS" data-content="${settings.ANIME_SPLIT_HOME_IN_TABS}">
        <meta data-var="settings.COMING_EPS_LAYOUT" data-content="${settings.COMING_EPS_LAYOUT}">
        <meta data-var="settings.COMING_EPS_SORT" data-content="${settings.COMING_EPS_SORT}">
        <meta data-var="settings.DATE_PRESET" data-content="${settings.DATE_PRESET}">
        <meta data-var="settings.FUZZY_DATING" data-content="${settings.FUZZY_DATING}">
        <meta data-var="settings.HISTORY_LAYOUT" data-content="${settings.HISTORY_LAYOUT}">
        <meta data-var="settings.HOME_LAYOUT" data-content="${settings.HOME_LAYOUT}">
        <meta data-var="settings.POSTER_SORTBY" data-content="${settings.POSTER_SORTBY}">
        <meta data-var="settings.POSTER_SORTDIR" data-content="${settings.POSTER_SORTDIR}">
        <meta data-var="settings.ROOT_DIRS" data-content="${settings.ROOT_DIRS}">
        <meta data-var="settings.SORT_ARTICLE" data-content="${settings.SORT_ARTICLE}">
        <meta data-var="settings.TIME_PRESET" data-content="${settings.TIME_PRESET}">
        <meta data-var="settings.TRIM_ZERO" data-content="${settings.TRIM_ZERO}">
        <meta data-var="settings.FANART_BACKGROUND" data-content="${settings.FANART_BACKGROUND}">
        <meta data-var="settings.FANART_BACKGROUND_OPACITY" data-content="${settings.FANART_BACKGROUND_OPACITY}">
        <%block name="metas" />

        <link rel="shortcut icon" href="${static_url('images/ico/favicon.ico')}">
        <link rel="icon" sizes="16x16 32x32 64x64" href="${static_url('images/ico/favicon.ico')}">
        <link rel="icon" type="image/png" sizes="196x196" href="${static_url('images/ico/favicon-196.png')}">
        <link rel="icon" type="image/png" sizes="160x160" href="${static_url('images/ico/favicon-160.png')}">
        <link rel="icon" type="image/png" sizes="96x96" href="${static_url('images/ico/favicon-96.png')}">
        <link rel="icon" type="image/png" sizes="64x64" href="${static_url('images/ico/favicon-64.png')}">
        <link rel="icon" type="image/png" sizes="32x32" href="${static_url('images/ico/favicon-32.png')}">
        <link rel="icon" type="image/png" sizes="16x16" href="${static_url('images/ico/favicon-16.png')}">
        <link rel="apple-touch-icon" sizes="152x152" href="${static_url('images/ico/favicon-152.png')}">
        <link rel="apple-touch-icon" sizes="144x144" href="${static_url('images/ico/favicon-144.png')}">
        <link rel="apple-touch-icon" sizes="120x120" href="${static_url('images/ico/favicon-120.png')}">
        <link rel="apple-touch-icon" sizes="114x114" href="${static_url('images/ico/favicon-114.png')}">
        <link rel="apple-touch-icon" sizes="76x76" href="${static_url('images/ico/favicon-76.png')}">
        <link rel="apple-touch-icon" sizes="72x72" href="${static_url('images/ico/favicon-72.png')}">
        <link rel="apple-touch-icon" href="${static_url('images/ico/favicon-57.png')}">

        <link rel="stylesheet" type="text/css" href="${static_url('css/vendor.min.css')}"/>
        <link rel="stylesheet" type="text/css" href="${static_url('css/browser.css')}" />
        <link rel="stylesheet" type="text/css" href="${static_url('css/lib/jquery-ui-1.10.4.custom.min.css')}" />
        <link rel="stylesheet" type="text/css" href="${static_url('css/lib/jquery.qtip-2.2.1.min.css')}"/>
        <link rel="stylesheet" type="text/css" href="${static_url('css/style.css')}"/>
        <link rel="stylesheet" type="text/css" href="${static_url('css/print.css')}" />

        %if settings.THEME_NAME != "light":
            <link rel="stylesheet" type="text/css" href="${static_url(urljoin('css/', '.'.join((settings.THEME_NAME, 'css'))))}" />
        %endif
        <%block name="css" />
    </head>
    <body>
        <nav class="navbar navbar-default navbar-fixed-top hidden-print">
            <div class="container-fluid">
                <div class="navbar-header">
                    <button type="button" class="navbar-toggle collapsed" data-toggle="collapse"
                            data-target="#nav-collapsed">
                        <span class="sr-only">${_('Toggle navigation')}</span>
                        <span class="icon-bar"></span>
                        <span class="icon-bar"></span>
                        <span class="icon-bar"></span>
                    </button>
                    <a class="navbar-brand" href="${static_url("apibuilder/", include_version=False)}" title="SickChill">
                        <img alt="SickChill" src="${static_url('images/sickchill.png')}" style="height: 50px;padding: 3px;" class="img-responsive pull-left" />
                        <p class="navbar-text hidden-xs">${title}</p>
                    </a>
                </div>

                <div class="collapse navbar-collapse" id="nav-collapsed">
                    <div class="btn-group navbar-btn" data-toggle="buttons">
                        <label class="btn btn-primary">
                            <input autocomplete="off" id="option-profile" type="checkbox"/> ${_('Profile')}
                        </label>
                        <label class="btn btn-primary">
                            <input autocomplete="off" id="option-jsonp" type="checkbox"/> ${_('JSONP')}
                        </label>
                    </div>

                    <ul class="nav navbar-nav navbar-right">
                        <li><a href="${static_url("home/", include_version=False)}">${_('Back to SickChill')}</a></li>
                    </ul>

                    <form class="navbar-form navbar-right">
                        <div class="form-group">
                            <input autocomplete="off" class="form-control" id="command-search"
                                   placeholder="Command name" type="search"/>
                        </div>
                    </form>
                </div>
            </div>
        </nav>
        <div id="content" class="container-fluid">
            <div class="panel-group" id="commands_list">
                % for command in sorted(commands):
                    <%
                        command_id = command.replace('.', '-')
                        command_help = commands[command]((), {'help': 1}).run()
                    %>
                    <div class="panel panel-default">
                        <div class="panel-heading">
                            <h4 class="panel-title">
                                <a data-toggle="collapse" data-parent="#commands_list"
                                   href="#command-${command_id}">${command}</a>
                            </h4>
                        </div>
                        <div class="panel-collapse collapse" id="command-${command_id}">
                            <div class="panel-body">
                                <div class="row">
                                    <div class="col-md-12">
                                        <blockquote>${command_help['message']}</blockquote>
                                    </div>
                                </div>
                                % if command_help['data']['optionalParameters'] or command_help['data']['requiredParameters']:
                                    <div class="row">
                                        <div class="col-md-12">
                                            <h4>${_('Parameters')}</h4>

                                            <div class="horizontal-scroll">
                                                <table class="tablesorter">
                                                    <thead>
                                                        <tr>
                                                            <th>${_('Name')}</th>
                                                            <th>${_('Required')}</th>
                                                            <th>${_('Description')}</th>
                                                            <th>${_('Type')}</th>
                                                            <th>${_('Default value')}</th>
                                                            <th>${_('Allowed values')}</th>
                                                        </tr>
                                                    </thead>
                                                    ${display_parameters_doc(command_help['data'], True)}
                                                    ${display_parameters_doc(command_help['data'], False)}
                                                </table>
                                            </div>
                                        </div>
                                    </div>
                                % endif
                                <div class="row">
                                    <div class="col-md-12">
                                        <h4>${_('Playground')}</h4>
                                        <span>URL:&nbsp;<kbd id="command-${command_id}-base-url">/api/${apikey}/?cmd=${command}</kbd></span>
                                    </div>
                                </div>
                                % if command_help['data']['requiredParameters']:
                                    <br/>
                                    <div class="row">
                                        <div class="col-md-12">
                                            <label>Required parameters</label>
                                            ${display_parameters_playground(command_help['data'], True, command_id)}
                                        </div>
                                    </div>
                                % endif
                                % if command_help['data']['optionalParameters']:
                                    <br/>
                                    <div class="row">
                                        <div class="col-md-12">
                                            <label>Optional parameters</label>
                                            ${display_parameters_playground(command_help['data'], False, command_id)}
                                        </div>
                                    </div>
                                % endif
                                <br/>
                                <div class="row">
                                    <div class="col-md-12">
                                        <button class="btn btn-primary" data-action="api-call" data-command-name="${command_id}"
                                                data-base-url="command-${command_id}-base-url"
                                                data-target="#command-${command_id}-response"
                                                data-time="#command-${command_id}-time" data-url="#command-${command_id}-url">
                                            Call API
                                        </button>
                                    </div>
                                </div>

                                <div class="result-wrapper hidden">
                                    <div class="clearfix">
                                        <span class="pull-left">
                                            Response: <strong id="command-${command_id}-time"></strong><br>
                                            URL: <kbd id="command-${command_id}-url"></kbd>
                                        </span>
                                        <span class="pull-right">
                                            <button class="btn btn-default" data-action="clear-result" data-target="#command-${command_id}-response">${_('Clear')}</button>
                                        </span>
                                    </div>
                                    <pre><code id="command-${command_id}-response"></code></pre>
                                </div>
                            </div>
                        </div>
                    </div>
                % endfor
            </div>
        </div>

        <script type="text/javascript">
            //noinspection JSUnusedLocalSymbols
            var episodes = ${ json.dumps(episodes) };
            //noinspection JSUnusedLocalSymbols
            var commands = ${ json.dumps(sorted(commands)) };
        </script>
        <script type="text/javascript" src="${static_url('js/vendor.min.js')}"></script>
        <script type="text/javascript" src="${static_url('js/core.min.js')}"></script>
        <script type="text/javascript" src="${static_url('js/apibuilder.js')}"></script>
    </body>
</html>

<%def name="display_parameters_doc(parameters, required)">
    <tbody>
        <%
            if required:
                parameter_list = parameters['requiredParameters']
            else:
                parameter_list = parameters['optionalParameters']
        %>
        % for parameter in parameter_list:
            <% parameter_help = parameter_list[parameter] %>
            <tr>
                <td>
                    % if required:
                        <strong>${parameter}</strong>
                    % else:
                        ${parameter}
                    % endif
                </td>
                <td class="text-center">
                    % if required:
                        <span class="glyphicon glyphicon-ok text-success" title="${_('Yes')}"></span>
                    % else:
                        <span class="glyphicon glyphicon-remove text-muted" title="${_('No')}"></span>
                    % endif
                </td>
                <td>${parameter_help.get('desc', '')}</td>
                <td>${parameter_help.get('type', '')}</td>
                <td>${parameter_help.get('defaultValue', '')}</td>
                <td>${parameter_help.get('allowedValues', '')}</td>
            </tr>
        % endfor
    </tbody>
</%def>

<%def name="display_parameters_playground(parameters, required, command)">
    <div class="form-inline">
        <%
            if required:
                # noinspection PyUnusedLocal
                parameter_list = parameters['requiredParameters']
            else:
                # noinspection PyUnusedLocal
                parameter_list = parameters['optionalParameters']
        %>
        % for parameter in parameter_list:
            <%
                parameter_help = parameter_list[parameter]
                allowed_values = parameter_help.get('allowedValues', '')
                type = parameter_help.get('type', '')
            %>

            % if isinstance(allowed_values, list):
                <select class="form-control"${('', ' multiple="multiple"')[type == 'list']} name="${parameter}" data-command="${command}">
                    <option>${parameter}</option>

                    % if allowed_values == [0, 1]:
                        <option value="0">${_('No')}</option>
                        <option value="1">${_('Yes')}</option>
                    % else:
                        % for allowed_value in allowed_values:
                            <option value="${allowed_value}">${allowed_value}</option>
                        % endfor
                    % endif
                </select>
            % elif parameter == 'indexerid':
                <select class="form-control" name="${parameter}" data-action="update-seasons" data-command="${command}">
                    <option>${parameter}</option>

                    % for show in shows:
                        <option value="${show.indexerid}">${show.name}</option>
                    % endfor
                </select>

                % if 'season' in parameters:
                    <select class="form-control hidden" name="season" data-action="update-episodes" data-command="${command}">
                        <option>${_('season')}</option>
                    </select>
                % endif

                % if 'episode' in parameters:
                    <select class="form-control hidden" name="episode" data-command="${command}">
                        <option>${_('episode')}</option>
                    </select>
                % endif
            % elif parameter == 'tvdbid':
                <input class="form-control" name="${parameter}" placeholder="${parameter}" type="number" data-command="${command}"/>
            % elif type == 'int':
                % if parameter not in ('episode', 'season'):
                    <input class="form-control" name="${parameter}" placeholder="${parameter}" type="number" data-command="${command}"/>
                % endif
            % elif type == 'string':
                <input class="form-control" name="${parameter}" placeholder="${parameter}" type="text" data-command="${command}"/>
            % endif
        % endfor
    </div>
</%def>