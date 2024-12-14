class Block:
    def __init__(self, size, start=0):
        self.size = size
        self.start = start
        self.allocated = False
        self.buddy = None

    def __str__(self):
        status = "Allocated" if self.allocated else "Free"
        return f"Block(Start: {self.start}, Size: {self.size}, Status: {status})"


class BuddySystem:
    def __init__(self, total_memory):
        self.total_memory = total_memory
        self.blocks = [Block(total_memory)]  # Initially one large block

    def split_block(self, block):
        size = block.size // 2
        left = Block(size, block.start)
        right = Block(size, block.start + size)
        left.buddy = right
        right.buddy = left
        self.blocks.remove(block)
        self.blocks.extend([left, right])
        print(f"Split: {block} -> {left}, {right}")
        return left

    def merge_block(self, block):
        buddy = block.buddy
        if buddy and not buddy.allocated and buddy.size == block.size:
            # Check if buddy block exists in the list before removal
            if buddy in self.blocks:
                merged = Block(block.size * 2, min(block.start, buddy.start))
                self.blocks.remove(block)
                self.blocks.remove(buddy)
                self.blocks.append(merged)
                print(f"Merged: {block}, {buddy} -> {merged}")
                # Recursively attempt to merge the newly created merged block with its buddy
                self.merge_block(merged)
            else:
                print(f"Buddy block {buddy} already merged or missing.")
        else:
            print(f"Cannot merge {block} with its buddy (either allocated or different size).")

    def allocate(self, size):
        for block in sorted(self.blocks, key=lambda b: b.size):
            if not block.allocated and block.size >= size:
                while block.size // 2 >= size:
                    block = self.split_block(block)
                block.allocated = True
                print(f"Allocated: {block}")
                return block
        print("No suitable block available!")
        return None

    def deallocate(self, start):
        for block in self.blocks:
            if block.start == start and block.allocated:
                block.allocated = False
                print(f"Deallocated: {block}")
                # Attempt to merge after deallocation
                self.merge_block(block)
                return
        print(f"Block at {start} not found or not allocated!")

    def display_blocks(self):
        print("Memory Blocks:")
        for block in sorted(self.blocks, key=lambda b: b.start):
            print(block)


if __name__ == "__main__":
    system = BuddySystem(128)  # Initialize with 128 units of memory

    print("\n--- Memory Allocation ---")
    system.allocate(50)
    system.allocate(20)
    system.display_blocks()

    print("\n--- Memory Deallocation ---")
    system.deallocate(0)
    system.display_blocks()

    print("\n--- Memory Deallocation Again ---")
    system.deallocate(64)
    system.display_blocks()
