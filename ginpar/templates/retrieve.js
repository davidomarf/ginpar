{% if global_seed -%}
function newRandomSeeds(){
    RANDOM_SEED = Math.random() * 100000000
    NOISE_SEED = Math.random() * 100000000
}
{%- endif %}


function resetDraw(){
    updateVars(); setup(); draw();
}

function updateVars(){
    {% for param in params -%}
        {%- if param["attrs"]['type'] == 'dimensions' -%}

        {{ param.var }} = [
                    Number(document.getElementById("{{ param.id }}-0").value),
                    Number(document.getElementById("{{ param.id }}-1").value)
                ];

        {% else %}
        
        {{ param.var }} = 
                {%- if param.attrs.type == "number" -%} Number{%- endif -%}
                (document.getElementById("{{param.id}}").value);
        {%- endif  %}
    {%- endfor %}

}
updateVars()
{{'\n'}}