import {
  bucket,
  spear,
  sword,
  musketeer as musketeerImg,
  warrior as warriorImg,
  bannerholder0,
} from "@/shared/assets";
import { Invader } from "../types/invader";

export const flagGrunt: Invader = {
  score: 250,
  health: 500,
  icon: bucket,
  typeCode: "G1",
};

export const spearGrunt: Invader = {
  score: 500,
  health: 1000,
  icon: spear,
  typeCode: "G2",
};

export const swordGrunt: Invader = {
  score: 1250,
  health: 2500,
  icon: sword,
  typeCode: "G3",
};

export const musketeer: Invader = {
  score: 15000,
  health: 25000,
  icon: musketeerImg,
  typeCode: "M",
};

export const warrior: Invader = {
  score: 50000,
  health: 50000,
  icon: warriorImg,
  typeCode: "W",
};

export const battleMage: Invader = {
  score: 750000,
  health: 500000,
  icon: bannerholder0,
  typeCode: "BW",
};

export const INVADERS_LIST = [
  flagGrunt,
  spearGrunt,
  swordGrunt,
  warrior,
  musketeer,
  battleMage,
];
