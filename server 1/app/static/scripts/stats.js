
$(()=>{
    $.get("/api/dashboard/stats?command=whoami", (res)=>{
      $("#connected-users p").text(res);
    });
  });
  