# DM_AssociationAnalysis

Project 1
Association Analysis









目錄
1.	Introduction、File structure
2.	Validation
3.	Kaggle Dataset Compare 
4.	IBM Dataset Compare
5.	Apriori hashtree
6.	Summary







Introduction 1
實做 Apriori 及 FP Growth 兩個演算法並應用在至少兩個資料集上，從kaggle找到Market Basket Optimization 資料集,包含7501份資料,並且使用IBM Quest Data Generator 生成包含8290筆的資料集合。此外對不同資料集,不同條件設計下,測量運算時間,進行比較。
1.	Kaggle  - Market Basket Optimization
2. 	IBM Quest Data Generator  - data.csv
 
File structure
 
Validation2
表格一為我使用兩種演算法所建立的 association rules，其中 minimum support =2%, minimum Confidence = 20%。它們各自產生的規則及運算數值可驗證我所建立的程式碼之正確性。
 
表一,兩種演算法對’ Kaggle’資料產生的 association rules

Kaggle Dataset Compare3
Use Apriori Algorithm
Low support,
Low confidence  
MinSupport	MinConf
15	0.6
1-itemset = 115    
2-itemset = 1225  
3-itemset= 1154  
4-itemset=170  
5-itemset=2
Time taken= 203.25ms 
	Low support,
High confidence   
MinSupport	MinConf
15	0.9
1-itemset = 115 
2-itemset = 1225 
3-itemset= 1154 
4-itemset=170 
5-itemset=2
6-itemset=1
Time taken= 215.62ms
High support, 
Low confidence  
MinSupport	MinConf
30	0.6
1-itemset = 114
2-itemset = 595	
3-itemset= 284
4-itemset=11
Time taken= 83.26ms	High support,
High confidence 
MinSupport	MinConf
30	0.9
1-itemset = 114
2-itemset = 595	
3-itemset= 284
4-itemset= 11
Time taken= 80.79ms
 
Use FP Growth
Low support, 
Low confidence 
MinSupport	MinConf
15	0.6
1-itemset = 115
2-itemset = 1219	
3-itemset= 1147
4-itemset= 170
5-itemset=2
Time taken= 0.95ms	Low support, 
High confidence 
MinSupport	MinConf
15	0.9
1-itemset = 115
2-itemset = 1219	
3-itemset= 1147
4-itemset= 170
5-itemset=2
Time taken= 0.95ms 
High support, 
Low confidence  
MinSupport	MinConf
30	0.6
1-itemset = 113
2-itemset = 587
3-itemset= 281
4-itemset= 11
Time taken= 0.84ms 	High support, 
High confidence  
MinSupport	MinConf
30	0.9
1-itemset = 113
2-itemset = 587
3-itemset= 281
4-itemset= 11
Time taken= 0.84ms 
 
圖 一、使用 Kaggle dataset 進行條件差別實驗之運算時間結果。
IBM Dataset Compare4
Use Apriori Algorithm
Low support, 
Low confidence 
MinSupport	MinConf
15	0.6
1-itemset = 144  
2-itemset = 143  
3-itemset= 87  
4-itemset=34 
5-itemset=8
6-itemset=1
Time taken= 7.88ms 	Low support, 
High confidence
MinSupport	MinConf
15	0.9
1-itemset = 144
2-itemset = 143
3-itemset= 87
4-itemset=34 
5-itemset=8
6-itemset=1
Time taken= 8.48ms 
High support, 
Low confidence  
MinSupport	MinConf
30	0.6
1-itemset = 17
2-itemset = 9	
3-itemset= 3
Time taken= 0.93ms 	High support, 
Low confidence
MinSupport	MinConf
30	0.9
1-itemset = 17
2-itemset = 9	
3-itemset= 3
Time taken= 0.93ms 
 
Use FP Growth
Low support, 
Low confidence 
MinSupport	MinConf
15	0.6
1-itemset = 143
2-itemset = 123
3-itemset= 50
4-itemset= 16
5-itemset=5
6-itemset=1
Time taken= 0.03m	low support, 
High confidence 
MinSupport	MinConf
15	0.9
1-itemset = 143
2-itemset = 123
3-itemset= 50
4-itemset= 16
5-itemset=5
6-itemset=1
Time taken= 0.03ms
High support, 
Low confidence 
MinSupport	MinConf
30	0.6
1-itemset = 16
2-itemset = 7
3-itemset= 2
Time taken= 0.02ms 	High support, 
High confidence
MinSupport	MinConf
30	0.9
1-itemset = 16
2-itemset = 7
3-itemset= 2
Time taken= 0.02ms
 
圖 一、使用IBM dataset 進行條件差別實驗之運算時間結果。
Apriori hashtree5
DataSet	MinSupport	max_leaf_count	max_child_count
IBM 	15	3	5
1-itemset = 144
2-itemset = 131	
3-itemset=76
4-itemset=29
5-itemset=7
6-itemset=1
Time taken= 0.225ms 
Summary6
Apriori是使用candidate_set搜尋frequent patterns,進行到每一層時都必須重新產生 candidate_set,並且花費大量資源在掃描資料庫;雖然apriori的缺點很明顯,但apriori的出現,改良了傳統完整掃描的方法,加快運算速度,也為datamining提供了一種新的想法。
FP-Growth 是由apriori 改良而成,採用樹狀結構,先構建出FPtree,再從FPtree中挖掘frequent itemset,減少掃描次數並且,fp-growth只需要做兩次掃描,而非apriori在每一層都生成candidate來進行掃描。 
 
表二、求不同min_sup，min_conf下，花費運算時間。
 
圖三、不同資料集長度、不同演算法的花費時間
