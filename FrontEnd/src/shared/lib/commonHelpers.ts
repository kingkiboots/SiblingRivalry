export const replaceArrayElOf = <T>(
  array: Array<T>,
  targetIndex: number,
  newEl: T
) => {
  return [
    ...array.slice(0, targetIndex),
    newEl,
    ...array.slice(targetIndex + 1, array.length),
  ];
};
