def calculateDeletionCRNodes(correspondingCR, nonDeletionIndex, maxdepth, deletedEventHasCR):
    casualRelItems = set()
    depthIndex = -1
    while(deletedEventHasCR and len(casualRelItems) < 1):
        casualRelItems = {cr[nonDeletionIndex]
                          for cr in correspondingCR if cr[2] <= depthIndex}
        depthIndex += 1
        if(depthIndex > maxdepth):
            print('Repair break loop, after reached max deepness:' + str(maxdepth))
            break
    return casualRelItems
