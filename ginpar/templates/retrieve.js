var RANDOM_SEED = Math.round(Math.random() * 100000000)
var NOISE_SEED = Math.round(Math.random() * 100000000)

{% if global_seed -%}
function ginpar_newRandomSeeds(){
    RANDOM_SEED = Math.round(Math.random() * 100000000)
    NOISE_SEED = Math.round(Math.random() * 100000000)
}
{%- endif %}


function ginpar_resetDraw(){
    ginpar_updateVars(); setup(); draw();
}

function ginpar_updateVars(){
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

function ginpar_save(){
    save(`${RANDOM_SEED}-${NOISE_SEED}`)
}

ginpar_updateVars()
{{'\n'}}