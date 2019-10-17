function updateVars(){
    {% for variable in attrs -%}
        {% if variable['attrs']['type'] == 'dimensions' -%}

        {{variable.var}} = [
                    document.getElementById("{{ variable.id }}-0").value,
                    document.getElementById("{{ variable.id }}-1").value
                ];

        {% else %}
        
        {{variable.var}} = document.getElementById("{{variable.id}}").value;

        {%- endif  %}
    {%- endfor %}

}
updateVars()
{{'\n'}}