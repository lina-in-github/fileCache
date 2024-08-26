// Define GameData[GlobalConst.COOKIE]
function init(){
if (!GlobalConst.COOKIE in GameData){
GameData[GlobalConst.COOKIE] = {
  PLAYER_HEALTH: 100,
  PLAYER_ATTACK_POWER: 20,
  PLAYER_DEFENSE: 10
};
}
}
// Define Player class
class Player {
  constructor(name, health, attackPower, defense) {
    this.name = name;
    this.health = health || GameData[GlobalConst.COOKIE].PLAYER_HEALTH;
    this.attackPower = attackPower || GameData[GlobalConst.COOKIE].PLAYER_ATTACK_POWER;
    this.defense = defense || GameData[GlobalConst.COOKIE].PLAYER_DEFENSE;
  }

  //TODO: Implement player actions
  attack(target) {
    const damage = this.attackPower - target.defense;
    if (damage > 0) {
      target.health -= damage;
      console.log(`${this.name} attacks ${target.name} for ${damage} damage!`);
    } else {
      console.log(`${this.name}'s attack is blocked by ${target.name}'s defense!`);
    }
  }
  save(COOKIE){
    GameData[COOKIE].PLAYER_HEALTH=this.health;
    GameData[COOKIE].PLAYER_ATTACK_POWER=this.attackPower;
    GameData[COOKIE].PLAYER_DEFENSE=this.defense;
  }
  move(position) {
    //TODO: Implement
    console.log(`${this.name} moves to ${position}!`);
  }

  defend() {
    //TODO: Implement
    console.log(`${this.name} defends!`);
  }
}

// Define the game map and positions for players
const gameMap = {
positions: [
    { name: 'position1', players: [] },
    { name: 'position2', players: [] },
    { name: 'position3', players: [] }
  ]
};
//TODO: add player groups logic
// Implement the game loop to handle player inputs and update the game state
// Implement logic to handle player attacking another player
// Use SetMenu to provide a menu for players to choose their actions
SetMenu({
  'attack': function() {
    //TODO: Implement logic to handle player attacking another player
  },
  'move': function() {
    //TODO: Implement logic to handle player moving to another position
    //TABNINE:implement it
    //GlobalConst.COOKIE
  },
  'defend': function() {
    //TODO: Implement logic to handle player defending

  },
  'quit': function() {
    delete GameData[GlobalConst.COOKIE];
    return('Thanks for playing!');
  }
});