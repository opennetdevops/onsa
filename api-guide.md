# API Guide

{% api-method method="post" host="" path="/api/login" %}
{% api-method-summary %}
JWT Authentication
{% endapi-method-summary %}

{% api-method-description %}
This endpoint allows you to get free cakes.
{% endapi-method-description %}

{% api-method-spec %}
{% api-method-request %}
{% api-method-headers %}
{% api-method-parameter name="Content-Type" type="string" required=true %}
Must be set to application/json
{% endapi-method-parameter %}
{% endapi-method-headers %}

{% api-method-body-parameters %}
{% api-method-parameter name="username" type="string" required=true %}
ONSA Username
{% endapi-method-parameter %}

{% api-method-parameter name="password" type="string" required=true %}
ONSA Password
{% endapi-method-parameter %}
{% endapi-method-body-parameters %}
{% endapi-method-request %}

{% api-method-response %}
{% api-method-response-example httpCode=200 %}
{% api-method-response-example-description %}
Cake successfully retrieved.
{% endapi-method-response-example-description %}

```javascript
{
    "token": "e8as78daskdjas7da9s.laskdlajshdagsdh1823.912837182yi3hkasd"
}
```
{% endapi-method-response-example %}
{% endapi-method-response %}
{% endapi-method-spec %}
{% endapi-method %}



