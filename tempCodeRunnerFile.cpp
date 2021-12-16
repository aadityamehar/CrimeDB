#include <iostream>
using namespace std;
void print(int heap[], int n){
for (int i = 0; i < n; i++){
cout << heap[i] << " ";
}
cout << "\n";
}
void insert(int heap[], int value, int n){
int i=n;
heap[n] = value;
n = n+1;
print(heap, n);
int parent;
while(i >= 0){
parent = (i-1)/2;
if(heap[parent] < heap[i]){
swap(heap[i], heap[parent]);
i = parent;
}
else{
break;
}
print(heap, n);
}
// cout << " out\t";
// print(heap, n);
}
void heapify(int heap[], int n, int i) {
int largest = i;
int left = 2 * i + 1;
int right = 2 * i + 2;
if (left < n && heap[left] > heap[largest])
largest = left;
if (right < n && heap[right] > heap[largest])
largest = right;
if (largest != i) {
swap(heap[i], heap[largest]);
heapify(heap, n, largest);
}
}
int main(){
int n, heap[10], i=0;
int element, k;

cout << "Enter the number of elements to insert: ";
cin >> n;
//insert(heap, 85, 4);
for(i = 0; i<n; i++){
cout << "Enter the element: ";
cin >> element;
insert(heap, element, i);
}
cout << "\n\nThe entire heap is: ";
print(heap, i);
n=n+4;
cout << "Heapsorted: ";
for (int i = n - 1; i >= 0; i--) {
swap(heap[0], heap[i]);
heapify(heap, i, 0);
}
print(heap, n);
cout << "Enter k: ";
cin >> k;
cout << "The kth smallest element is: ";
cout << heap[k-1];
cout <<"\nThe kth largest element is: ";
cout << heap[n-k];
return 0;
}