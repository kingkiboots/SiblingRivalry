import { useAppDispatch, useAppSelector } from "@/shared/redux/hooks";
import { INVADERS_LIST, setGameBoard } from "@/entities/mechanics";
import { Grid, Heading } from "@chakra-ui/react";
import { DragEventHandler } from "react";
import { UnitCell, UnitCellGridItem } from "@/shared/ui";
import { replaceArrayElOf } from "@/shared/lib";
import { grayTile, redTile } from "@/shared/assets";

export const MainGameBoardWidget = () => {
  const gameBoard = useAppSelector((state) => state.gameBoard.value);
  const dispatch = useAppDispatch();

  const handleDragOver: DragEventHandler = (e) => {
    e.preventDefault();
  };

  const handleDrop: DragEventHandler = (e) => {
    e.preventDefault();
    const currentIndex = parseInt(
      (e.currentTarget as HTMLElement).dataset.index ?? "-1"
    );

    if (currentIndex === -1) {
      console.debug(
        "[MainGameBoardWidget,handleDrop] currentIndex is undefined",
        e.currentTarget
      );
      return;
    }

    const invaderTypeCode = e.dataTransfer.getData("typeCode");
    const invaderObjectToAdd = INVADERS_LIST.find(
      (invader) => invader.typeCode === invaderTypeCode
    );

    if (!invaderObjectToAdd) {
      console.debug(
        "[MainGameBoardWidget,handleDrop] No Found invaderObjectToAdd by",
        invaderTypeCode
      );
      return;
    }

    dispatch(
      setGameBoard(
        replaceArrayElOf(gameBoard, currentIndex, {
          ...invaderObjectToAdd,
          onBoardStatus: "on",
        })
      )
    );
  };

  return (
    <>
      <Heading as="h3" size="md" textAlign="center" width="100%">
        Main Game Board
      </Heading>
      <Grid templateColumns="repeat(5, 1fr)" p={4} bg="purple.900">
        {gameBoard.map((invader, index) => {
          const isEven = index % 2 === 0;
          return (
            <UnitCellGridItem
              key={index}
              w="60px"
              h="60px"
              backgroundImage={isEven ? redTile : grayTile}
              data-index={index}
              onDragOver={handleDragOver}
              onDrop={handleDrop}
              opacity={invader?.onBoardStatus === "hover" ? 0.5 : 1}
            >
              <UnitCell invader={invader} />
            </UnitCellGridItem>
          );
        })}
      </Grid>
    </>
  );
};
