let locationAddress = document.querySelector(".address").innerText;
var locations = [];
locations.push(["", `${locationAddress}`]);

var geocoder, infowindow;
var markers = [];
function initMap() {
  infowindow = new google.maps.InfoWindow();
  geocoder = new google.maps.Geocoder();

  var myLatlng = { lat: -25.363, lng: 131.044 };
  var map = new google.maps.Map(document.getElementById("map"), {
    zoom: 17,
    center: myLatlng,
    mapTypeId: google.maps.MapTypeId.ROADMAP,
  });
  if (geocoder) {
    addMarkers(map, geocoder, locations, function () {
      // finished added
    });
  }
}

window.initMap = initMap;

function addMarkers(map, geocoder, addresses, callback) {
  var coords = [];
  for (var i = 0; i < addresses.length; i++) {
    geocoder.geocode({ address: addresses[i][1] }, function (results, status) {
      if (status == google.maps.GeocoderStatus.OK) {
        coords.push(results[0].geometry.location);
        let mylat = results[0].geometry.location.lat();
        let mylong = results[0].geometry.location.lng();
        locations.pop();
        locations.push([
          `<a type=_blank class=location href=https://maps.google.com/maps?ll=${mylat},${mylong}&z=20&t=m&hl=en-US&gl=US&mapclient=apiv3>View In maps </a> <br/> ${locationAddress} <br/>&#160`,
          `${locationAddress}`,
        ]);
        var pos = coords.length;
        if (coords.length == 1) {
          map.setCenter(results[0].geometry.location);
        }
        if (coords.length == addresses.length) {
          if (typeof callback == "function") {
            callback();
          }
        }
        var marker = new google.maps.Marker({
          map: map,
          position: results[0].geometry.location,
          icon:
            "https://chart.apis.google.com/chart?chst=d_map_pin_letter_withshadow&chld=" +
            (i + 0) +
            "|FFB200|31404C",
        });

        marker.addListener("click", function () {
          infowindow.setContent(addresses[pos - 1][0]);
          infowindow.open(map, marker);
        });
      } //if (status == google.maps.GeocoderStatus.OK) {
    });
  }
}
