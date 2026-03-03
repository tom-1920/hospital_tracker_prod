function getLocation() {
  if (!navigator.geolocation) {
    alert("Location not supported");
    return;
  }
  navigator.geolocation.getCurrentPosition(function(position) {
    const lat=position.coords.latitude;
    const lon=position.coords.longitude;
      window.location.href =`/lat=${lat}&lon=${lon}`;
  });
