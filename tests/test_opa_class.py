import pytest
import responses

from flask_opa import AccessDeniedException


@responses.activate
def test_get_home_page_granted(app):
    opa_url = app.config.get('OPA_URL')
    responses.add(responses.POST, opa_url,
                  json={'result': True}, status=200)

    response = app.test_client().get('/')

    assert 0 < len(response.data)
    assert 200 == response.status_code


@responses.activate
def test_opa_grant_access(app):
    opa_url = app.config.get('OPA_URL')
    responses.add(responses.POST, opa_url, json={'result': True}, status=200)

    response = app.test_client().get('/')

    assert 0 < len(response.data)
    assert 200 == response.status_code


@responses.activate
def test_opa_denies_access(app):
    opa_url = app.config.get('OPA_URL')
    responses.add(responses.POST, opa_url, json={'result': False}, status=200)

    response = app.test_client().post('/')

    assert 403 == response.status_code


@responses.activate
def test_opa_server_unavailable_should_deny_access(app):
    opa_url = app.config.get('OPA_URL')
    responses.add(responses.POST, opa_url, status=404)

    response = app.test_client().post('/')

    assert 403 == response.status_code

@pytest.mark.xfail(raises=ValueError)
def test_app_with_missing_url(app_with_missing_url):
    pass


@responses.activate
@pytest.mark.xfail(raises=AccessDeniedException)
def test_app_secured_from_configuration(app_secured_from_configuration):
    opa_url = app_secured_from_configuration.config.get('OPA_URL')
    responses.add(responses.POST, opa_url, json={'result': False}, status=200)

    app_secured_from_configuration.test_client().post('/')
