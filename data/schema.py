import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyConnectionField, SQLAlchemyObjectType
from models import db_session, Category as CategoryModel,Product as ProductModel, Offer as OfferModel,User as UserModel
from sqlalchemy import and_	

class Users(SQLAlchemyObjectType):
	class Meta:
	    model = UserModel
	    interfaces = (relay.Node, )

# Used to Create New User
class createUser(graphene.Mutation):
	class Input:
		name = graphene.String()
		email = graphene.String()
		username = graphene.String()
	ok = graphene.Boolean()
	user = graphene.Field(Users)

	@classmethod
	def mutate(cls, _, args, context, info):
		user = UserModel(name=args.get('name'), email=args.get('email'), username=args.get('username'))
		db_session.add(user)
		db_session.commit()
		ok = True
		return createUser(user=user, ok=ok)
# Used to Change Username with Email
class changeUsername(graphene.Mutation):
	class Input:
		username = graphene.String()
		email = graphene.String()

	ok = graphene.Boolean()
	user = graphene.Field(Users)

	@classmethod
	def mutate(cls, _, args, context, info):
		query = Users.get_query(context)
		email = args.get('email')
		username = args.get('username')
		user = query.filter(UserModel.email == email).first()
		user.username = username
		db_session.commit()
		ok = True

		return changeUsername(user=user, ok = ok)

class Product(SQLAlchemyObjectType):
	class Meta:
	    model = ProductModel
	    interfaces = (relay.Node, )

# Used to Create New Product
class createProduct(graphene.Mutation):
	class Input:
		name = graphene.String()
		description=graphene.String()
		author_id = graphene.Int()
	
		category_id =  graphene.Int()
	ok = graphene.Boolean()
	product = graphene.Field(Product)
	@classmethod
	def mutate(cls, _, args, context, info):
		product = ProductModel(name=args.get('name'), description=args.get('description'),author_id=args.get('author_id'), category_id=args.get('category_id'))
		db_session.add(product)
		db_session.commit()
		ok = True
		return createProduct(product=product, ok=ok)



class Category(SQLAlchemyObjectType):
	class Meta:
	    model = CategoryModel
	    interfaces = (relay.Node, )

# Used to Create New Category
class createCategory(graphene.Mutation):
	class Input:
		name = graphene.String()
	ok = graphene.Boolean()
	category = graphene.Field(Category)

	@classmethod
	def mutate(cls, _, args, context, info):
		category = CategoryModel(name=args.get('name'))
		db_session.add(category)
		db_session.commit()
		ok = True
		return createCategory(category=category, ok=ok)

class Offer(SQLAlchemyObjectType):
	class Meta:
	    model = OfferModel
	    interfaces = (relay.Node, )

# Used to Create New Offer
class createOffer(graphene.Mutation):
	class Input:	
		amount = graphene.Float()
		offerdescription = graphene.String()
		product_id = graphene.Int()
		user_id = graphene.Int()
		
	ok = graphene.Boolean()
	offer = graphene.Field(Offer)

	@classmethod
	def mutate(cls, _, args, context, info):
		offer = OfferModel(amount=args.get('amount'),offerdescription=args.get('offerdescription'),product_id=args.get('product_id'),user_id=args.get('user_id'))
		db_session.add(offer)
		db_session.commit()
		ok = True
		return createOffer(offer=category, ok=ok)


class Query(graphene.ObjectType):
	node = relay.Node.Field()
	user = SQLAlchemyConnectionField(Users)
	find_user = graphene.Field(lambda: Users, username = graphene.String())
	all_users = SQLAlchemyConnectionField(Users)

	def resolve_find_user(self,args,context,info):
		query = Users.get_query(context)
		username = args.get('username')
		# you can also use and_ with filter() eg: filter(and_(param1, param2)).first()
		return query.filter(UserModel.username == username).first()


class MyMutations(graphene.ObjectType):
	create_user = createUser.Field()
	create_product = createProduct.Field()
	create_offer = createOffer.Field()
	create_category = createCategory.Field()

	change_username = changeUsername.Field()

schema = graphene.Schema(query=Query, mutation=MyMutations, types=[Users])
