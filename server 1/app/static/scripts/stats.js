
$(()=>{
    $.get("/api/dashboard/stats?command=whoami", (res)=>{
      
      $("#connected-users p").text(res);
      $("#new-orders p").text()
      $("#total-trafic p").text()
    });
  });
  