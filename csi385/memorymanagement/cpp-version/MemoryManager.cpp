#include "MemoryManager.h"

MemoryManager::MemoryManager(uint capacity)
{
    mHead = new Node(0, capacity, "free memory", true);
}

Node* MemoryManager::findEmptySpaceForProcess(uint size)
{
    Node *temp;

    if(mHead != NULL){
        if(mHead->mIsEmpty){
            return mHead;
        }

        temp = mHead->mNext;
        while(temp != NULL){
            temp->mIsEmpty && size <= temp->mSize ? return temp : temp = temp->mNext;
        }

        return NULL;
    }

}

void MemoryManager::allocate(string name, uint size)
{
    Node* freespace = findEmptySpaceForProcess(size);

    if(freespace == NULL){
        //out error not enought space
        return;
    }

    Node* newNode = new Node(freespace->mStart, size, name, false);

    if(size < freespace->mSize){
        freespace->mSize -= (size);
        freespace->mStart = (size - 1);

        if(frees)

    }



}
