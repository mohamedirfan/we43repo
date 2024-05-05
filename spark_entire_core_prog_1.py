print("What we are going to learn here"
      "1. Important - How to create a spark application - sparkSession object to enter into spark application"
      "2. Not Important - How to create RDDs - multiple methods"
      "3. Not Important -Different types of transformations, characteristics of transformations and its usage"
      "4. Not Important -Characteristics of action and its usage"
      "5. Important - Spark Architecture, Core fundamentals, Performance Optimization etc.,"
      "Out of all above 5 components in spark core (component 1 and 5 are important, rest of the components 2,3,4 can be just learned once for attending interviews and for supplementing component 5")

print("1. How to create a spark application - sparkSession object to enter into spark application")
#To start write a spark application, we need sparkcontext, sqlcontext, hivecontext hence we are instantiating sparksession
#Interview question: How you are gettin spark session object created or importance of spark session or how you start write a spark application?
from pyspark.sql.session import SparkSession
#spark=SparkSession.builder.getOrCreate()#minimum needed
spark=SparkSession.builder.master("local[*]").appName("WE43 Spark Core App").enableHiveSupport().getOrCreate()
#SparkSession.builder -> class Builder -> methods master/appname/enablehivesupport/getorcreate -> SparkSession object created
#SparkSession is a class
#builder is a class variable/attribute used to call the functions like master, appname,enablehivesupport, getorcreate to build this sparksession object
#master - help us submit this spark application to the respective cluster manager
#appName - help us name this application to uniquely identify in web gui when it runs in cluster
#enablehivesupport - used to enble hive context to write complete HQL with most of the feature like catalog, udfs etc.,
#getorcreate - help us get an existing spark session already running or help us create a new spark session object.

#Lets understand how SparkSession.builder.getOrCreate() works...
print("Existing spark object",spark)

spark1=SparkSession.builder.getOrCreate()
print("New spark object (Existing)",spark1)

spark.stop()
spark2=SparkSession.builder.getOrCreate()
print("New spark object (New)",spark2)


print("2. Not Important - How to create RDDs using multiple methodologies - "
      "still we need to learn this to understand what is RDD, how memory management & partition management is happening fundamentally")
spark2.stop()
from pyspark.sql.session import SparkSession
spark=SparkSession.builder.master("local[*]").appName("WE43 Spark Core App").enableHiveSupport().getOrCreate()
sc=spark.sparkContext

#Interview Questions:
#Can we have more than one spark context in a same application? No, only one can be created
#Error org.apache.spark.SparkException: Only one SparkContext should be running in this JVM (see SPARK-2243).The currently running SparkContext was created at:


#There are 4 ways we can create RDDs -
# 1.RDDs can be created from some sources
# 2.RDDs can be created from another RDD
# 3.RDDs can be created from memory
# 4.RDDs can be created programatically
#Terminologies to remember before learning about RDDs - RDD, DAG (Direct Acyclick Graph), Lineage (direct relation between RDDs as transformation and action), transformation , action
#What is RDD? Resilient (Can be Rebuild) Distributed (across muliple nodes memory) Dataset (can come from anywhere)
#Real life simple realization - In a hotel (cluster), Tables (nodes), in plates (containers) customers (spark transformations & actions) are filling food (dataset) and sit in different tables (distributed)
#The food can be filled from different food counters (data)
#sit in different tables (distributed)
#in case if they lost the plate it can be refilled (resilient)
#customers (spark transformations & actions) - Transformations - filling food in the plate, adding curry, mixing, joining, aggregating... Actions - eating/drinking/filtering/chewing/tasting
#hotel is managed by manager (cluster manager - standalone/mesos/kb/yarn/local)

#Why we need RDD? For performing lighning speed inmemory computation in a parallel & distributed fashion in the cluster on the large scale data
#RDDs are fault tolerant via lineage inside the DAG?
#RDDs are Distributed using partitions?

print("1.RDDs can be created from some file sources - Initial RDD creation")
file_rdd1=sc.textFile("file:///home/hduser/cust.txt")#textfile takes input of a file location and returns RDD
hadoop_rdd1=sc.textFile("/user/hduser/cust.txt")
print("Total number of customers we have",file_rdd1.count())

#A spark application can be developed with minimum an rdd performed with an action (transformation is optional)

print("2.RDDs can be created from another RDD from memory (refreshed/recreated) - To transform one RDD to Another because RDDs are immutable")
function1=lambda row:"chennai" in row #Python Anonymous lambda function or we can create python named defined method
def met1(row):
      return "chennai" in row
another_rdd2=hadoop_rdd1.filter(function1) #Filter is what type of function? Higher Order Function
#hivetable1 fname,lname(non modifyable) -> insert select concat(fname,lname) where city='chennai' -> another hivvetable fullname

print("3.RDDs can be created another RDD from memory (retained) (important)- Usually when an rdd is materialized from storage layer to memory, by default"
      "it will be deleted by Garbage Collector, by applying cache on the given RDD (which requires reuse) the GC will not clean the data")
file_rdd1=sc.textFile("file:///home/hduser/cust.txt")
file_rdd1.cache()#When the first action executed on file_rdd1 or the child rdds of file_rdd1, then data will retained in the cahce rather than dleting
another_rdd2=file_rdd1.filter(function1)
another_rdd2.count()#first time when action is performed the data will come from the disk -> rdd1 (memory retained)-> rdd2 (memory cleaned) -> action
#If cached, the rdd does not show the new count if dataset is updated
another_rdd2.count()#second time onwards when action is performed the data will come from the rdd1 (memory retained) -> rdd2 -> action
file_rdd1.unpersist() #clean the memory for others to consume
#After action completion ..do we need to remove the retained memory
#Yes, If we still have some more lines of code writtened in this application where we don't have any dependency on the cached rdd file_rdd1
#No, If the line number 86 is the last line of this application, then when spark session is closed, automatically the memory objects will be removed.

file_rdd2=sc.textFile("file:///home/hduser/empdata.csv")
print(file_rdd2.count())

print("4.RDDs can be created programatically - When we wanted to convert the given data into rdd or when we do development with some sample dataset")
#1.When we want to convert the given data into RDD
customerData = [
    (1, "John", 1000, "Chennai"),
    (2, "Mary", 2000, "Bangalore"),
    (3, "Tom", 1500, "Chennai"),
    (4, "Emma", 3000, "Mumbai"),
    (5, "Peter", 2500, "Chennai")
]

# Create an RDD from the list of customer data
customerRDD = sc.parallelize(customerData)
print(customerRDD.count())

#2. For development or testing or learning we want to create RDD programatically...
lst=range(1,1001)
rdd1=sc.parallelize(lst,10)
print(rdd1.glom().collect())


print("3. How to Transform/process RDDs - Not much important")

#Interview Question: How to identify the given function is a transformation or an action?
#If a function returns another rdd then it is transformation
#If a function returns result/value then it is action
rdd1=sc.parallelize(range(1,101))
rdd2=rdd1.map(lambda val:val+.5)#This map is a transformation function as it returns another rdd"
print("This map is a transformation function as it returns another rdd",rdd2)
print("This count is an action function as it returns result", rdd2.sum())

#Interview Question: Transformation are of 2 categories
#Active Transformation - If the output number of elements of a given rdd is different from the input number of elements of an rdd
print(rdd1.count())
rdd2=rdd1.filter(lambda x:x>=10)
print(rdd2.count())
print("If False then filter is a active transformation ",rdd1.count()==rdd2.count())
#Passive Transformation - If the output number of elements of a given rdd is same as like the input number of elements of an rdd
print(rdd1.count())
rdd2=rdd1.map(lambda val:val+.5)
print(rdd2.count())
print("If True then map is a passive transformation ",rdd1.count()==rdd2.count())

#Interview Question:
#Transformations Dependency Characteristics (spark CM, job, task, stage)
#Narrow Dependent Transformations
#Wide Dependent Transformations

#Let's learn about few important transformations (we don't use in spark SQL development),
# but we may rarely use in spark core application #development eg. unstructured data management, data cleanup etc.,
# or for understanding the core architecture/terminologies better or for attending the interviews this learning may be useful
#map, flatmap, filter, zip, zipwithindex, set transformations, join, reducebykey...

#map transformation: map is a higher of method, used to apply any functionality/transformation on every element of a given RDD.
#map is equivalent to a for/while loop but it is a distributed & parallel function that can run on rdd partitions concurrently...
#In SQL side: map is equivalent to select in SQL.
sal_lst=[10000,20000,15000,30000]
bon=1000
new_sal_lst=[]
for sal in sal_lst:
    new_sal_lst.append(sal+bon)#sequencially

sal_lst_rdd=sc.parallelize([10000,20000,15000,30000],2)
bon=1000
lam_func=lambda sal:sal+bon
rdd2=sal_lst_rdd.map(lam_func)#distributedly/parallely/concurrently across partitions using in memory

#I want to split the list(string) to list(list(string)) to list(list(some defined datatype)), we can use map deliberately
rdd1=sc.textFile("file:///home/hduser/empdata.csv")
print("list(string)",rdd1.collect())
rdd2=rdd1.map(lambda elem:elem.split(","))
print("list(list(string))",rdd2.collect())
rdd3=rdd2.map(lambda x:[int(x[0]),int(x[2]),x[1]])
print("list(list(some defined datatype))",rdd3.collect())

#Usecase: I dont need column 2 in the given dataset, i need to identify the right datatype for the col1 and col3?
rdd1=sc.textFile("file:///home/hduser/empdata.csv")

#filter transformation:
# filter is a higher of method, used to apply any conditions on every actual element or transformed element of a given RDD.
#filter equivalent construct in python is ? forloop and if condition
#filter equivalent in DB is ? select and where clause

sal_lst=[10000,20000,15000,30000]
#I wanted to filter the sal >=20000
for sal in sal_lst:
    if sal>=20000:
        print(sal)

rdd1=sc.parallelize([10000,20000,15000,30000],2)
rdd2=rdd1.filter(lambda x:x>=20000)#Filter will iterate every element as like map, then apply condition if returns True then
# filter allow the element to the next rdd, else ignore that element
print(rdd2.collect())

rdd1=sc.textFile("file:///home/hduser/empdata.csv")
rdd2=rdd1.map(lambda elem:elem.split(","))
rdd3=rdd2.filter(lambda x:int(x[2])>=20000)#transforming x[2] to int type
print(rdd3.collect())

#Usecase for standardization of data using spark core programming: map and filter function? I need the output of type int,string,int with 3 columns, if less than 3 columns, ignore it
#101,raja,10000
#102,vinay,15000
#103,karthik
#104
#We wanted to reject unwanted data and create rdd with 3 columns data then convert to dataframe asap
rdd1=sc.textFile("file:///home/hduser/empdata1.csv").map(lambda x:x.split(","))
rdd2=rdd1.filter(lambda x:len(x)==3)
print(rdd2.collect())
spark.createDataFrame(rdd2).toDF("id","name","sal").show()

#flatmap transformation (active):
# flatmap is a higher of method, used to iterate on the given list of values and flatten it (transpose it) like explode function in DB
# flatmap runs nested for loops when comparing with python programming
lst1=["hadoop spark hadoop kafka","hadoop datascience java cloud"]
flat_lst=[]
for i in lst1:
 for j in i.split(" "):
  flat_lst.append(j)
  print(j)
# flatmap uses select and explode functionalities as like SQL
rdd1=sc.textFile("file:///home/hduser/sparkdata/courses.log")
rdd2=rdd1.flatMap(lambda x:x.split(" "))

#Interview Question: Difference between map and flatMap?
#map will iterate at the first level (rows), flatmap will iterate 2 levels (rows and columns)
#map is to apply any transformation on every elements, flatmap is to apply transpose/flatten on every elements
#map can be applied on structured, flatmap can be applied on both type of struct or unstructured data also.

#Write a word count program using spark core? How to identify the occurance of the given words in a unstructured dataset?
rdd1=sc.textFile("file:///home/hduser/sparkdata/courses.log")
rdd2=rdd1.flatMap(lambda x:x.split(" "))
print(rdd2.countByValue())

#zipWithIndex - is used for adding index sequence into the elements of the RDD
#In python I want to display both element and the index value? enumerate(lst)
#In SQL we need the row and the row_number? row_number() over()
print(rdd1.zipWithIndex().collect())
#Realtime usage of zipwithindex

#Interview question: How to do you remove the header from a given dataset?
print(rdd1.zipWithIndex().filter(lambda x:x[1]>0).map(lambda x:x[0]).collect())

#Transformations that operates between RDDs

#zip (passive) and zipwithindex (passive) transformations
#zip is used to unconditionally merge/join the data horizontally with other dataset which doesn't have any identified to join
#thumb rules to use zip - the number of partitions and the partition elements between the rdd should be same
'''
1,irfan,42
2,xyz,40
3,abc,30

Chennai,IT
Banglore,MKT
Mumbai,IT
'''
rdd1=sc.textFile("file:///home/hduser/custmaster").map(lambda x:x.split(",")).map(lambda x:[x[0],x[1],x[2]])
rdd2=sc.textFile("file:///home/hduser/custdetail").map(lambda x:x.split(",")).map(lambda x:[x[0],x[1]])
rdd1.zip(rdd2).map(lambda x:(x[0][0],x[0][1],x[0][2],x[1][0],x[1][1])).collect()

#set functions (union (unionall), intersection, subtract) - all set are active trans
rdd1=sc.textFile("file:///home/hduser/custmaster1")
rdd2=sc.textFile("file:///home/hduser/custmaster2")

#union (will not ignore duplicates) will act like union all in DB (active)
print(rdd1.union(rdd2).collect())

#union with distinct will act like a union in DB (ignore duplicates) (active)
#I want to deduplicate the duplicate data in the given RDD or I wanted to implement union (deduplicated) rather than union all?
print(rdd1.union(rdd2).distinct().collect())

#intersection (active) - used to identify the common data between the rdds
print(rdd1.intersection(rdd2).collect())

#subtract (active) - used to subract an rdd from another rdd
print(rdd1.subtract(rdd2).collect())
print(rdd1.subtract(rdd2).collect())

#paired RDD - An RDD that contains the data in a form of key,value pair, then it is paired RDD.
#Certain Transformations (paired rdd transformations)/actions (paired rdd actions) only work on paired rdds, hence paired rdds are used in spark

#Eg. of paired RDD and paired RDD Transformations
#join is a paired rdd transformation, works only on paired rdd
#We can join multiple rdds using spark core join paired rdd transformation, but not much preferred rather it is preferred to
#execute joins using spark sql (because it is optimized by default using catalyst optimizer in spark sql)
rdd1=sc.textFile("file:///home/hduser/custmaster1").map(lambda x:x.split(",")).map(lambda x:(x[0],(x[1],x[2])))
rdd2=sc.textFile("file:///home/hduser/custdetail").map(lambda x:x.split(",")).map(lambda x:(x[2],(x[0],x[1])))
rdd1.join(rdd1).collect()#self
rdd1.join(rdd2).collect()#inner
rdd1.leftOuterJoin(rdd2).collect()#left
rdd1.rightOuterJoin(rdd2).collect()#right
rdd1.fullOuterJoin(rdd2).collect()#full

#reduceByKey is a paired rdd transformation, works only on paired rdd
#I need to reduce the result based on the key, we use reducebykey transformation
#reduceByKey will work like reduce action, reduceByKey work based on the key the reduction will happen but reduce will do reduction based on values
rdd1=sc.textFile("file:///home/hduser/hive/data/txns").map(lambda x:x.split(",")).map(lambda x:(x[7],float(x[3])))
#rdd1.reduceByKey()
lam=lambda b,f:b if b>f else f
print("state wise max of sales",rdd1.reduceByKey(lam).take(3))
lam=lambda b,f:b if b<f else f
print("state wise sum of sales min sales",rdd1.reduceByKey(lam).take(3))
lam=lambda b,f:b+f
print("state wise sum of sales",rdd1.reduceByKey(lam).take(3))
#Interview Questions: Difference between reduce and reducebykey, difference between countbykey and reducebykey
#difference between groupbykey and reducebykey...

print("Dependent Transformations : Narrow (map, filter) & Wide Dependent (reducebykey, join) Transformations")
#Narrow dependent Transformation
rdd1=sc.textFile("file:///home/hduser/hive/data/txns").map(lambda x:x.split(",")).filter(lambda x:x[7]=='California')
#Wide dependent Transformation
rdd1=sc.textFile("file:///home/hduser/hive/data/txns").map(lambda x:x.split(",")).map(lambda x:(x[7],float(x[3])))
rdd2=rdd1.reduceByKey(lambda x,y:x+y)
rdd2.collect()
#txns=100000 -> 50k(p1-map1)-500 Cal, 50k(p2-map2)-1000 Cal -> reducebykey1 Cal,[500+1000]
#txns=100000 -> 50k(p1-map1)-1500 Ten, 50k(p2-map2)-1000 Ten -> reducebykey2 Ten,[1500+1000]


print("4. How to Materialize/Actions RDDs - Not much important")
#Action is an RDD function/method used to return the result/value to the driver or to the storage layer
#collect action - Used to collect the rdd elements as a result to the Driver.

#Interview Questions: collect action has to be causiously used or avoid using collect because?
#collect bring all data from multiple executors to one driver, hence consumption of resources like network and memory is high
#collect may reduce the performance of the application when used on a large of volume of data
#collect may break the application with OOM exception when used on a large of volume of data
#alternative for collect?? - sampling, storage in disk, take, first, top, count ...
#Conclusion: Collect should be used for development, testing or in Production (if it is inevitable)
rdd1=sc.textFile("/user/hduser/custs")
len(rdd1.collect())
print("costly effort as we are collecting all data to driver, then counting sequencially using python len function",len(rdd1.collect()))
print(rdd1.count())
print("less cost effort as we are counting parallely/distributedly and returning the count and not the data, "
      "then consolidating by running count in the driver finally on the partial counts and not on the data",rdd1.count())

#Other alternative actions for collect if we want to see the data (few, one, ordered, sample)
print(rdd1.take(3))
#Random sampling transformation
print(rdd1.takeSample(True,3,2))#used for random sampling - withreplacement-True will ensure to return unique samples, num (total samples), seed (controlling of random samples using seed value)
print(rdd1.takeOrdered(3))#Ascending order of sorting and take the top values
print(rdd1.first())
print(rdd1.top(3))#Descending order of sorting and take the top values

#Usecase: Interview question: How to do you remove the header from a given dataset using take, first?
'''
id,name,age
1,irfan,42
2,aaa,30
'''

#quick usecase to understand all 4 parts of spark core?
#Defining spark session, creating rdds, transforming rdd, action perfomed
#Define spark session object / sc
#Create an RDD from the file:///usr/local/hadoop/logs/hadoop-hduser-namenode-localhost.localdomain.log
#Apply transformation to filter only ERROR and WARN data from the above rdd
#Store the error data in /user/hduser/errdata/ and warning data in /user/hduser/warndata/
#part1
from pyspark.sql.session import SparkSession
spark = SparkSession.builder.master("local[*]").appName("Spark log parsing").getOrCreate()
sc = spark.sparkContext
#part2
file_rdd1=sc.textFile("file://usr/local/hadoop/logs/hadoop-hduser-namenode-localhost.localdomain.log").map(lambda x:x.split(" "))
#part3
filtered_rdd=file_rdd1.filter(lambda x:len(x)>=2)
#file_rdd1=sc.textFile("file:///usr/local/hadoop/logs/hadoop-hduser-namenode-localhost.localdomain.log")
#err_rdd=file_rdd1.filter(lambda x:'ERROR' in x)
#warn_rdd=file_rdd1.filter(lambda x:'WARN' in x)
err_rdd=filtered_rdd.filter(lambda x:x[2]=='ERROR')
warn_rdd=filtered_rdd.filter(lambda x:x[2]=='WARN')
#part4
err_rdd.saveAsTextFile("/user/hduser/errdata")
warn_rdd.saveAsTextFile("/user/hduser/warndata")

#code in a single line
#sc.textFile("file://usr/local/hadoop/logs/hadoop-hduser-namenode-localhost.localdomain.log").map(lambda x:x.split(" ")).filter(lambda x:len(x)>=2).filter(lambda x:x[2]=='ERROR').saveAsTextFile("/user/hduser/errdata")
#sc.textFile("file://usr/local/hadoop/logs/hadoop-hduser-namenode-localhost.localdomain.log").map(lambda x:x.split(" ")).filter(lambda x:len(x)>=2).filter(lambda x:x[2]=='WARN').saveAsTextFile("/user/hduser/warndata")


print("running countbyvalue,countbykey etc.,")
rdd1=sc.textFile("/user/hduser/custs").map(lambda x:x.split(","))
rdd2=rdd1.map(lambda x:x[4])
print(rdd2.countByValue())

#Actions also of type paired rdd actions - Actions work on paired rdd is paired rdd actions like lookup, countByKey, combineByKey etc.,
#CountByKey is a paired rdd action, since it requires the key,value pair rdd as an input
#CountByKey will be used to count the occurance of the key
rdd2=rdd1.map(lambda x:(x[4],int(x[3])))
rdd2.countByKey()#paired RDD Action

#lookup is a paired rdd action, since it requires the key,value pair rdd as an input
#lookup is used for getting the result for the given key passed as an argument (it is an alternative for left join)
#lookup and enrichment - lookup for the customerid and enrich the customer name
rdd2=rdd1.map(lambda x:(x[0],(x[1],x[2])))
rdd2.lookup('4000001')

#reduce() action help us reduce/consolidate/combine the result in any customized way we needed the result
#lambda function, lambda service in cloud, lambda architecture for data management
#How the name lambda has been brought in?
#3 5 8
#8 8
#16
lam=lambda b,f:b if b>f else f
rdd1=sc.textFile("file:///home/hduser/hive/data/txns").map(lambda x:x.split(",")).filter(lambda x:x[7]=='California').map(lambda x:float(x[3]))
lam=lambda b,f:b+f
def met1(b,f):
    return b+f
print("sum of amt",rdd1.reduce(lam))
rdd1.sum()
rdd1.min()
lam=lambda b,f:b if b<f else f
print("max of amt",rdd1.reduce(lam))
lam=lambda b,f:b if b>f else f
print("max of amt",rdd1.reduce(lam))
rdd1.max()

#Can you write word count program in spark core?




#Important (Core/SQL/Stream)- 5. Spark Arch/terminologies (first cut), Performance Optimization, Job Submission, Spark Cluster concept (VV Important) - not used only for core, used in SQL & Streaming also
print("5. Spark Arch/terminologies, Performance Optimization, Job Submission, Spark Cluster concept (VV Important) - not used only for core, used in SQL & Streaming also")
#Performance Optimization (foundation concepts)- primary activity
#pluck the Low hanging fruits
#1. Remove all unwanted (costly) actions performed while doing the development like collect & print/take/count... and use it if it is really needed
#Removal of dead codes/dormant codes, removal of the unused rdds

#2. Partition management - When creating RDDs (naturally and customized), before/after transformation , before performing action
#What is Partitioning -
# Partitioning the Horizontal division of data
#Partitioning is used for defining the degree of parallelism and distribution
#Partition help us distribute the data (in terms of spark partition help us distribute the data across multiple nodes in memory, in a form of RDD partitions)

#by default while creating RDDs -
# random (number of rows in a partition) partitioning or range of size of data
# coalesce - range partitioning (range of values in a given partition) or data size is random/different in diff partitions
# repartition (internally coalesce(shuffle=True)) - round robin  partitioning

#Partition management - when creating RDDs (how by default the number of partitions are assigned)



#Partition management - when creating RDDs (how to change the partitions)


#How do we manage/handle/change the number of partitions before/after performing transformations

#Scenario1 (increase partitions)
#Scenario2 (reduce partition)


#Interview Questions
#How the repartition and coalesce is working internally to distribute the partitions (range, round robin, random)
#When we have use repartition & coalesce, which is more preferred for reducing the number of partitions?
#How do you produce the output as a single file in spark?
#How to find the number of elements in a given rdd?
#How to find the number of elements in the each partition of a given rdd?

print("Increased Partition wise rows count using Repartition",
      "1. Repartition uses Round Robin Distribution, hence we will equal partition size "
      "2. Repartition will do shuffling (by default) or redistribution of data (hence costly function to use)"
      "3. Repartition is a costly function to use (use it causiously), only for increasing the number of partition use repartition, not for reducing")

print("Decreased Partition wise rows count using coalesce",
      "1. Coalesce uses Random Distribution (partitions will be merged), hence equal partition size cannot be assured"
      "2. Coalesce preferably will not do shuffling (but shuffling may happen at times) , hence coalaese is less cost"
      "3. Coalesce is a less cost function is supposed to use for reducing the number of partitions")


#Interview Question: How to do count the number of elements at the partition level



#3. Memory Optimization - Performance Optimization using Cache/Persist once RDD is created


#Few limitations/challenges in Caching:
#1. If the underlying data of the cached is changed, then we may not get expected results (happens on streaming applications)
# to overcome this issue, we can use checkpoint rather than cache
#2. Caching has to considered with other factors like volume of data, availability of resource, time taken for serialization/deserialization etc.
#3. Caching has to be used appropriately and cleaned appropriately
#4. Use cache appropriately before actions are performed on the parent or child rdds.
#5. Usage of the right type of cache in the name of persist is supposed to be considered.

#Interview Question: I have RAM less than the data in HDD, can we still process that data using Spark?
#Yes, Internally spark only bring the data into the RAM upto how much allocated, rest will be in disk and brought iteratively

#What is the differece between cache and persist?


#Broadcasting - Important to know for interview and for usage especially in the spark optimized joins
#Broadcasting is the concept of broadcast something that is referred/used/consumed by the consumers frequently/anonymousle/randomly
#Real life Eg. radio, video live streaming
#Interview Question? Have you used broadcasting in spark or Did you tried optimized joins in spark SQL?
# Spark Broadcasting is the special static variable that can broadcasted once for all from driver to worker (executors),
#hence spark rdd partition rows can refer that broadcasted variable locally rather than getting it from driver for every iteration


#Interview Question? How much data can be collected to the driver at given point of time?
#How much rows a rdd or variable can be to be broadcasted?
#It depends upon the capacity of the driver memory allocation

#Accumulator - Not much important in general usage, but needed for some interview discussions
#Accumulator is special incremental variable used for accumulating the number of tasks performed by the executors
#Accumulator is used to identify the progress completion of tasks running the in the respective exe3cutors...



##We have completed Spark Core - All 5 components, performance optimization
# (basic best practices, partitioning, memory managment, broadcast & accumulator)
# we will see more in detail (very very important) - (we see everything else including what you ask or dont ask)