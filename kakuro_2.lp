\ Model kakuro
\ LP format - for model browsing. Use MPS format to capture full model detail.
Minimize
 
Subject To
 Vertical_Sum_at_(0,2): G[1,2,0] + 2 G[1,2,1] + 3 G[1,2,2] + 4 G[1,2,3]
   + 5 G[1,2,4] + 6 G[1,2,5] + 7 G[1,2,6] + 8 G[1,2,7] + 9 G[1,2,8] = 3
 ColUniqueness_at_(0,2): G[1,2,0] <= 1
 ColUniqueness_at_(0,2): G[1,2,1] <= 1
 ColUniqueness_at_(0,2): G[1,2,2] <= 1
 ColUniqueness_at_(0,2): G[1,2,3] <= 1
 ColUniqueness_at_(0,2): G[1,2,4] <= 1
 ColUniqueness_at_(0,2): G[1,2,5] <= 1
 ColUniqueness_at_(0,2): G[1,2,6] <= 1
 ColUniqueness_at_(0,2): G[1,2,7] <= 1
 ColUniqueness_at_(0,2): G[1,2,8] <= 1
 RightSum_at_(1,0): G[1,1,0] + 2 G[1,1,1] + 3 G[1,1,2] + 4 G[1,1,3]
   + 5 G[1,1,4] + 6 G[1,1,5] + 7 G[1,1,6] + 8 G[1,1,7] + 9 G[1,1,8]
   + G[1,2,0] + 2 G[1,2,1] + 3 G[1,2,2] + 4 G[1,2,3] + 5 G[1,2,4]
   + 6 G[1,2,5] + 7 G[1,2,6] + 8 G[1,2,7] + 9 G[1,2,8] = 4
 RowUniqueness_at_(1,0): G[1,1,0] + G[1,2,0] <= 1
 RowUniqueness_at_(1,0): G[1,1,1] + G[1,2,1] <= 1
 RowUniqueness_at_(1,0): G[1,1,2] + G[1,2,2] <= 1
 RowUniqueness_at_(1,0): G[1,1,3] + G[1,2,3] <= 1
 RowUniqueness_at_(1,0): G[1,1,4] + G[1,2,4] <= 1
 RowUniqueness_at_(1,0): G[1,1,5] + G[1,2,5] <= 1
 RowUniqueness_at_(1,0): G[1,1,6] + G[1,2,6] <= 1
 RowUniqueness_at_(1,0): G[1,1,7] + G[1,2,7] <= 1
 RowUniqueness_at_(1,0): G[1,1,8] + G[1,2,8] <= 1
Bounds
Binaries
 G[1,1,0] G[1,1,1] G[1,1,2] G[1,1,3] G[1,1,4] G[1,1,5] G[1,1,6] G[1,1,7]
 G[1,1,8] G[1,2,0] G[1,2,1] G[1,2,2] G[1,2,3] G[1,2,4] G[1,2,5] G[1,2,6]
 G[1,2,7] G[1,2,8]
End
