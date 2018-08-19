const move = function(x,y,game_id) {
  $.ajax({
    type: "POST",
    url: '/move',
    data: {x: x, y: y, game_id: game_id},
    success: function(response) {
      $('#board').html(response);
    },
    error: function(error) {
      console.log(error);
      location.reload(true);
    }
  });
}

const refresh = function(game_id) {
  $.ajax({
    type: "GET",
    url: '/board/' + game_id,
    success: function(response) {
      $('#board').html(response);
    },
    error: function(error) {
      console.log(error);
      location.reload(true);
    }
  });
}

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

async function run(game_id) {
  await sleep(5000);
  refresh(game_id);
  run(game_id);
}

const choice = function(encounter_id, data) {
  $.ajax({
    type: "POST",
    url: `/encounter/${encounter_id}`,
    data: data,
    success: function(response) {
      location.reload(true);
    },
    error: function(error) {
      console.log(error);
    }
  });
}
