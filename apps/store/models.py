from django.db import models

    # public class Category : EntityBase
    # {
    #     public string Name { get; set; }
    #     public virtual Category ParentCategory { get; set; }
    #     public virtual List<Category> SubCategories { get; set; }
    #     public virtual List<Product> Products { get; set; }
    #     public virtual List<ProductDetail> ProductDetails { get; set; }
    # }
# Категория
class Category(models.Model):
    name = models.CharField(max_length=50, null=False, help_text="Наименование категории")


    # childCategories = models.ManyToOneRel()
    #
    #     /// <summary>
    # /// Товар
    # /// </summary>
    # public class Product : EntityBase
    # {
    #     public string Name { get; set; }
    #
    #     public string Description { get; set; }
    #
    #     public virtual Category Category { get; set; }
    #
    #     public virtual Manufacturer Manufacturer { get; set; }
    #
    #     public virtual ProductStatus ProductStatus { get; set; }
    #
    #     public virtual ApplicationUser Seller { get; set; }
    #
    #     public virtual File MainImage { get; set; }
    #
    #     public virtual List<File> Files { get; set; }
    #
    #     public virtual List<Comment> Comments { get; set; }
    #
    #     public virtual List<Rating> Ratings { get; set; }
    #
    #     /// <summary>
    #     /// Значение характеристик товара
    #     /// </summary>
    #     public virtual List<ProductDetailValue> ProductDetailValues { get; set; }
    #
    #     /// <summary>
    #     /// Строки заказа
    #     /// </summary>
    #     public virtual List<OrderPosition> OrderPositions { get; set; }
    # }


    # /// <summary>
    # /// Характеристика товара
    # /// </summary>
    # public class ProductDetail : EntityBase
    # {
    #     public string Name { get; set; }
    #
    #     public virtual Category Category { get; set; }
    #
    #     public virtual List<ProductDetailValue> ProductDetailValues { get; set; }
    # }


    #     /// <summary>
    # /// Значение характеристики товара
    # /// </summary>
    # public class ProductDetailValue : EntityBase
    # {
    #     public string StringValue { get; set; }
    #
    #     public virtual Product Product { get; set; }
    #
    #     public virtual ProductDetail ProductDetail { get; set; }
    # }

    #     public class Rating : EntityBase
    # {
    #     public int Value { get; set; }
    #
    #     public virtual Product Product { get; set; }
    #
    #     public virtual ApplicationUser CreatedBy { get; set; }
    # }

    #     /// <summary>
    # /// Строка заказа
    # /// </summary>
    # public class OrderPosition : EntityBase
    # {
    #     public int Quantity { get; set; }
    #
    #     public decimal Price { get; set; }
    #
    #     public virtual Product Product { get; set; }
    #
    #     public virtual Order Order { get; set; }
    # }


    #     public class Order : EntityBase
    # {
    #     public virtual OrderStatus OrderStatus { get; set; }
    #
    #     public virtual ApplicationUser Customer { get; set; }
    #
    #     public virtual ApplicationUser Seller { get; set; }
    #
    #     /// <summary>
    #     /// Строки заказа
    #     /// </summary>
    #     public virtual List<OrderPosition> OrderPositions { get; set; }
    # }

    #     public class Manufacturer : EntityBase
    # {
    #     public string Name { get; set; }
    #
    #     public string Address { get; set; }
    #
    #     public string Phone { get; set; }
    #
    #     public string Email { get; set; }
    #
    #     public virtual List<Product> Products { get; set; }
    # }

    #    public class File : EntityBase
    # {
    #     [DataType(DataType.Text)]
    #     [StringLength(100)]
    #     [Display(Name = "Name")]
    #     public string Name { get; set; }
    #
    #     public string ContentType { get; set; }
    #
    #     public byte[] Content { get; set; }
    #
    #     public virtual Product Product { get; set; }
    #
    #     public virtual List<Product> Products { get; set; }
    # }

    #     public class Comment : EntityBase
    # {
    #     public string Text { get; set; }
    #
    #     public virtual Product Product { get; set; }
    #
    #     public virtual ApplicationUser CreatedBy { get; set; }
    # }