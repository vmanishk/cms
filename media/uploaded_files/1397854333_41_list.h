typedef int bool;
#define true 1
#define false 0

struct II{
	int data;
	struct II* next;
}

int inOrder(struct II* list);

bool addc(struct II* list, int c);

void insertToPlace(struct II* list, int val, int place);