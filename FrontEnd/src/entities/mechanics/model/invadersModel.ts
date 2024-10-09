import {
  bucket,
  spear,
  sword,
  musketeer as musketeerImg,
  warrior as warriorImg,
  bannerholder0,
} from "@/shared/assets";
import { Invader } from "../types/invader";
import {
  INVADERS_TYPE_CODE_FLAG_GRUNT,
  INVADERS_TYPE_CODE_SPEAR_GRUNT,
  INVADERS_TYPE_CODE_SWORD_GRUNT,
  INVADERS_TYPE_CODE_MUSKETEER,
  INVADERS_TYPE_CODE_WARRIOR,
  INVADERS_TYPE_CODE_BATTLE_MAGE,
} from "../consts/invadersConsts";

export const flagGrunt: Invader = {
  score: 250,
  health: 500,
  icon: bucket,
  typeCode: INVADERS_TYPE_CODE_FLAG_GRUNT,
};

export const spearGrunt: Invader = {
  score: 500,
  health: 1000,
  icon: spear,
  typeCode: INVADERS_TYPE_CODE_SPEAR_GRUNT,
};

export const swordGrunt: Invader = {
  score: 1250,
  health: 2500,
  icon: sword,
  typeCode: INVADERS_TYPE_CODE_SWORD_GRUNT,
};

export const musketeer: Invader = {
  score: 15000,
  health: 25000,
  icon: musketeerImg,
  typeCode: INVADERS_TYPE_CODE_MUSKETEER,
};

export const warrior: Invader = {
  score: 50000,
  health: 50000,
  icon: warriorImg,
  typeCode: INVADERS_TYPE_CODE_WARRIOR,
};

export const battleMage: Invader = {
  score: 750000,
  health: 500000,
  icon: bannerholder0,
  typeCode: INVADERS_TYPE_CODE_BATTLE_MAGE,
};

export const INVADERS_LIST = [
  flagGrunt,
  spearGrunt,
  swordGrunt,
  warrior,
  musketeer,
  battleMage,
];
