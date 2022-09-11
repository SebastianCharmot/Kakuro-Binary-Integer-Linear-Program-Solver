\ Model kakuro
\ LP format - for model browsing. Use MPS format to capture full model detail.
Minimize
  0 G[1,1,0] + 0 G[1,1,1] + 0 G[1,1,2] + 0 G[1,1,3] + 0 G[1,1,4]
   + 0 G[1,1,5] + 0 G[1,1,6] + 0 G[1,1,7] + 0 G[1,1,8] + 0 G[1,2,0]
   + 0 G[1,2,1] + 0 G[1,2,2] + 0 G[1,2,3] + 0 G[1,2,4] + 0 G[1,2,5]
   + 0 G[1,2,6] + 0 G[1,2,7] + 0 G[1,2,8]
Subject To
Bounds
Binaries
 G[1,1,0] G[1,1,1] G[1,1,2] G[1,1,3] G[1,1,4] G[1,1,5] G[1,1,6] G[1,1,7]
 G[1,1,8] G[1,2,0] G[1,2,1] G[1,2,2] G[1,2,3] G[1,2,4] G[1,2,5] G[1,2,6]
 G[1,2,7] G[1,2,8]
End
