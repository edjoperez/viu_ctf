
$(()=>{
    $.get("/api/dashboard/stats?command=cat ../assets/stats.json", (res)=>{
      const stats = JSON.parse(res);
      $("#lastUpdate p").text(stats.lastUpdate)
      $("#connected-users p").text(stats.connectedUsers);
      $("#new-orders p").text(stats.newOrders);
      $("#total-trafic p").text(stats.totalTraffic)
    });
  });
  