
function   next(){
	{% if rows.has_next %}
    page={{ rows.next_page_number }};
    {% endif %}
    $.ajax({
    	type:"POST",
    	url:"{% url 'get_play' %}",
    	data:{"page":page},        
    	success:function(data){
    		 $("#jobs_table").html(data);    
         }
    })
}

function pre(){
	 {% if rows.has_previous %}
	   page={{ rows.previous_page_number }};
	　{% endif %}
	  $.ajax({
		  type:"POST",
		  url:"{% url 'get_play' %}",
		  data:{"page":page},         
		  success:function(data){
			  $("#jobs_table").html(data);    
	        }
	      
	               
	 })
	
}