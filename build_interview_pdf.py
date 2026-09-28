import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas

W = letter[0] - 108  # usable content width

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super(NumberedCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []
    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()
    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)
    def draw_page_number(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 7.5)
        self.setFillColor(colors.HexColor("#555555"))
        if self._pageNumber > 1:
            self.drawString(54, letter[1] - 36, "BookHub — Complete Technical Documentation & Interview Master Guide")
            self.setStrokeColor(colors.HexColor("#dddddd"))
            self.setLineWidth(0.5)
            self.line(54, letter[1] - 42, letter[0] - 54, letter[1] - 42)
            page_text = f"Page {self._pageNumber} of {page_count}"
            self.drawRightString(letter[0] - 54, 36, page_text)
            self.drawString(54, 36, "Java 21 | Spring Boot 4.0.5 | Spring Data JPA | Hibernate | MySQL | REST | HTML/CSS/JS")
            self.line(54, 48, letter[0] - 54, 48)
        self.restoreState()

# ─── helpers ───────────────────────────────────────────────────────────────
def cb(code_text, style, bg="#f8f9fa", border="#ced4da"):
    """create a code block"""
    esc = code_text.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace("\n","<br/>").replace("  ","&nbsp;&nbsp;")
    p = Paragraph(f"<font face='Courier' size='7'>{esc}</font>", style)
    t = Table([[p]], colWidths=[W])
    t.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,-1),colors.HexColor(bg)),
        ('BOX',(0,0),(-1,-1),0.5,colors.HexColor(border)),
        ('LEFTPADDING',(0,0),(-1,-1),8),('RIGHTPADDING',(0,0),(-1,-1),8),
        ('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5),
    ]))
    return t

def callout(text, style, title="KEY TAKEAWAY", bg="#eef6fb", border="#2b75a0"):
    content = [
        Paragraph(f"<b>{title}</b>", ParagraphStyle('CH', parent=style, fontName='Helvetica-Bold', fontSize=8, leading=10, textColor=colors.HexColor(border))),
        Spacer(1,2),
        Paragraph(text, style)
    ]
    t = Table([[content]], colWidths=[W])
    t.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,-1),colors.HexColor(bg)),
        ('BOX',(0,0),(-1,-1),1,colors.HexColor(border)),
        ('LEFTPADDING',(0,0),(-1,-1),10),('RIGHTPADDING',(0,0),(-1,-1),10),
        ('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5),
    ]))
    return t

def flow_box(lines, style, bg="#fefce8", border="#ca8a04"):
    """flow diagram box"""
    escaped_lines = [l.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;") for l in lines]
    txt = "<br/>".join(escaped_lines)
    p = Paragraph(txt, ParagraphStyle('Flow', parent=style, fontName='Courier', fontSize=7.5, leading=10.5, textColor=colors.HexColor("#1a1a1a")))
    t = Table([[p]], colWidths=[W])
    t.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,-1),colors.HexColor(bg)),
        ('BOX',(0,0),(-1,-1),1,colors.HexColor(border)),
        ('LEFTPADDING',(0,0),(-1,-1),10),('RIGHTPADDING',(0,0),(-1,-1),10),
        ('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6),
    ]))
    return t

# ─── MAIN ──────────────────────────────────────────────────────────────────
def generate_pdf():
    fname = "BookHub_Complete_Documentation_and_Interview_Guide.pdf"
    doc = SimpleDocTemplate(fname, pagesize=letter, leftMargin=54, rightMargin=54, topMargin=54, bottomMargin=54)
    styles = getSampleStyleSheet()

    # styles
    ts = ParagraphStyle('CT', parent=styles['Heading1'], fontName='Helvetica-Bold', fontSize=20, leading=24, textColor=colors.HexColor("#1d3557"), spaceAfter=4)
    sub = ParagraphStyle('CS', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=10, leading=14, textColor=colors.HexColor("#457b9d"), spaceAfter=12)
    h1 = ParagraphStyle('H1', parent=styles['Heading1'], fontName='Helvetica-Bold', fontSize=13, leading=17, textColor=colors.HexColor("#1d3557"), spaceBefore=12, spaceAfter=6, keepWithNext=True)
    h2 = ParagraphStyle('H2', parent=styles['Heading2'], fontName='Helvetica-Bold', fontSize=10.5, leading=14, textColor=colors.HexColor("#2a9d8f"), spaceBefore=8, spaceAfter=3, keepWithNext=True)
    h3 = ParagraphStyle('H3', parent=styles['Heading3'], fontName='Helvetica-Bold', fontSize=9, leading=12, textColor=colors.HexColor("#e76f51"), spaceBefore=6, spaceAfter=2, keepWithNext=True)
    b = ParagraphStyle('B', parent=styles['Normal'], fontName='Helvetica', fontSize=8.5, leading=12, textColor=colors.HexColor("#222222"), spaceAfter=4)
    bl = ParagraphStyle('BL', parent=styles['Normal'], fontName='Helvetica', fontSize=8, leading=11.5, textColor=colors.HexColor("#222222"), leftIndent=10, spaceAfter=3)
    cf = ParagraphStyle('CF', parent=styles['Code'], fontName='Courier', fontSize=7, leading=9.5, textColor=colors.HexColor("#1a1a1a"))
    cb_style = ParagraphStyle('CB', parent=styles['Normal'], fontName='Helvetica', fontSize=8, leading=11, textColor=colors.HexColor("#264653"))

    S = []

    # ═══════════════════════════════════════════════════════════════════════
    # COVER
    # ═══════════════════════════════════════════════════════════════════════
    S.append(Paragraph("BookHub — Complete Technical Documentation<br/>&amp; Comprehensive Interview Master Guide", ts))
    S.append(Paragraph("Every Tech Stack | Every File | Every Function | Every Line of Code | Every Workflow | Every Database Query — Fully Explained", sub))
    S.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor("#1d3557"), spaceAfter=10))
    mt = [
        [Paragraph("<b>Project:</b> BookHub Online Bookstore",b), Paragraph("<b>Backend:</b> Java 21 / Spring Boot 4.0.5",b)],
        [Paragraph("<b>Database:</b> MySQL 8.x + Spring Data JPA / Hibernate ORM",b), Paragraph("<b>Frontend:</b> Vanilla HTML5, CSS3, JavaScript Fetch API",b)],
        [Paragraph("<b>Architecture:</b> 3-Tier Layered MVC REST",b), Paragraph("<b>Build Tool:</b> Apache Maven (pom.xml)",b)],
        [Paragraph("<b>JDBC Driver:</b> mysql-connector-j",b), Paragraph("<b>Connection Pool:</b> HikariCP (auto-configured)",b)],
        [Paragraph("<b>Server:</b> Embedded Apache Tomcat (port 8080)",b), Paragraph("<b>Serialization:</b> Jackson JSON ObjectMapper",b)],
    ]
    mt_t = Table(mt, colWidths=[W/2.0, W/2.0])
    mt_t.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,-1),colors.HexColor("#f1f5f9")),
        ('BOX',(0,0),(-1,-1),1,colors.HexColor("#cbd5e1")),
        ('INNERGRID',(0,0),(-1,-1),0.5,colors.HexColor("#e2e8f0")),
        ('LEFTPADDING',(0,0),(-1,-1),6),('RIGHTPADDING',(0,0),(-1,-1),6),
        ('TOPPADDING',(0,0),(-1,-1),4),('BOTTOMPADDING',(0,0),(-1,-1),4),
    ]))
    S.append(mt_t)
    S.append(Spacer(1,8))

    # TABLE OF CONTENTS
    S.append(Paragraph("<b>Table of Contents</b>", h2))
    toc = [
        "Section 1 — Tech Stack: Interview Answers ('I used X to do Y')",
        "Section 2 — Project File Structure & What Each File Does",
        "Section 3 — How the Application Accesses MySQL (Complete Database Pipeline)",
        "Section 4 — How Frontend Connects to Backend (Complete HTTP Lifecycle)",
        "Section 5 — File-by-File & Function-by-Function Code Breakdown (With Full Code)",
        "Section 6 — End-to-End Workflow: What Happens When Each Action Is Selected",
        "Section 7 — Master REST API Reference Table & SQL Query Map",
        "Section 8 — CRUD Operations Explained With Code",
        "Section 9 — Exception Handling Pipeline",
        "Section 10 — Interview Closing Summary & Golden Pitch",
    ]
    for i,t in enumerate(toc):
        S.append(Paragraph(f"&bull; {t}", bl))
    S.append(PageBreak())

    # ═══════════════════════════════════════════════════════════════════════
    # SECTION 1: TECH STACK
    # ═══════════════════════════════════════════════════════════════════════
    S.append(Paragraph("Section 1 — Technology Stack: Interview Answers", h1))
    S.append(Paragraph("For each technology used in BookHub, memorize this first-person answer format:", b))
    S.append(Spacer(1,3))

    tech = [
        ("1. Java 21 (Programming Language)",
         "I used Java 21 as the primary programming language for my BookHub backend. Java is an object-oriented, strongly typed language that runs on the Java Virtual Machine (JVM). I chose Java 21 because it supports modern features like records, pattern matching, and virtual threads, and it provides high performance and cross-platform compatibility."),
        ("2. Spring Boot 4.0.5 (Backend Framework)",
         "I used Spring Boot 4.0.5 as the backend framework to build production-ready REST APIs rapidly. Spring Boot provides auto-configuration — it automatically detects dependencies like Spring Data JPA and MySQL Connector on the classpath and configures DataSource, EntityManager, and Hibernate without me writing XML or boilerplate. It also bundles an embedded Apache Tomcat server so I don't need to install a separate web server."),
        ("3. Spring Data JPA (Data Access Abstraction)",
         "I used Spring Data JPA to implement the data persistence layer. Instead of writing manual JDBC code with Connection, PreparedStatement, and ResultSet, I simply created Java interfaces (BookRepository, CartRepository, OrderRepository) that extend JpaRepository. Spring Data JPA automatically generates the SQL implementation at runtime using dynamic proxies."),
        ("4. Hibernate ORM (Object-Relational Mapping Engine)",
         "I used Hibernate as the ORM provider underneath Spring Data JPA. Hibernate automatically maps my Java entity classes (Book.java, CartItem.java, Order.java) to MySQL database tables. When I annotate a class with @Entity, Hibernate creates or updates the corresponding table. When I call repository.save(), Hibernate generates the INSERT or UPDATE SQL query automatically."),
        ("5. MySQL 8.x (Relational Database)",
         "I used MySQL as the relational database to persistently store all application data. I have three tables: 'book' (catalog inventory), 'cart_item' (temporary shopping cart state with a foreign key to book), and 'orders' (permanent purchase transaction history). MySQL provides ACID transactions, foreign key integrity, and efficient indexed queries."),
        ("6. MySQL Connector/J — mysql-connector-j (JDBC Driver)",
         "I used mysql-connector-j as the JDBC driver dependency in my pom.xml. This is the official MySQL JDBC driver that allows the Java Virtual Machine to establish a TCP network socket connection to the MySQL server running on localhost:3306 and execute SQL commands over that connection."),
        ("7. HikariCP (JDBC Connection Pool)",
         "I used HikariCP as the high-performance JDBC connection pool. It is auto-configured by spring-boot-starter-data-jpa. Instead of opening a new TCP database connection for every single HTTP request (which is very slow), HikariCP maintains a pool of pre-established connections. When a repository method needs to run SQL, it borrows a connection from the pool, executes the query, and returns it to the pool."),
        ("8. Spring Web MVC — spring-boot-starter-webmvc (REST Framework)",
         "I used Spring Web MVC to expose RESTful HTTP endpoints. Spring MVC uses the DispatcherServlet pattern — a front controller that intercepts all incoming HTTP requests, consults handler mappings to find the matching @RestController method, deserializes JSON request bodies using Jackson, invokes the controller method, and serializes the return value back into a JSON HTTP response."),
        ("9. Embedded Apache Tomcat (Servlet Container / Web Server)",
         "I used the embedded Apache Tomcat server that comes bundled with Spring Boot. It starts automatically when I run the application and listens on port 8080 (configured in application.properties). Tomcat accepts TCP connections from web browsers, forwards HTTP requests to Spring's DispatcherServlet, and sends HTTP responses back to the client."),
        ("10. REST API (Communication Protocol Pattern)",
         "I used REST APIs (Representational State Transfer) to create a stateless client-server communication interface. I designed resource-based URL endpoints like /books, /cart, and /orders and mapped them to standard HTTP methods: GET for reading data, POST for creating data, and DELETE for removing data. All data is exchanged in JSON format."),
        ("11. JSON (Data Exchange Format) & Jackson (Serializer)",
         "I used JSON (JavaScript Object Notation) as the standard data format for all communication between the frontend HTML pages and the Spring Boot backend. Jackson ObjectMapper, which is included by default in Spring Boot, automatically converts Java objects to JSON strings (serialization) when sending responses, and converts incoming JSON request bodies back into Java objects (deserialization)."),
        ("12. DTO Pattern — ApiResponse&lt;T&gt; (Data Transfer Object)",
         "I created a generic ApiResponse&lt;T&gt; class as a Data Transfer Object to standardize all API responses. Every endpoint in my application returns the same structure: { \"success\": true/false, \"message\": \"...\", \"data\": ... }. This ensures the frontend always knows exactly what format to expect, whether the operation succeeded or failed."),
        ("13. Vanilla HTML5 &amp; CSS3 (Frontend UI)",
         "I used plain HTML5 and CSS3 (without React, Angular, or Vue) to build two web pages: index.html (customer storefront) and admin.html (admin dashboard). I used CSS Grid for responsive book card layouts, CSS Flexbox for header alignment, CSS transitions for smooth cart drawer sliding animation, and gradient backgrounds for modern visual design."),
        ("14. JavaScript Fetch API (Frontend HTTP Client)",
         "I used the native JavaScript Fetch API with async/await syntax to send HTTP requests from the browser to my Spring Boot backend REST APIs. Fetch is built into all modern browsers — no external library like Axios is needed. I use fetch() for GET, POST, and DELETE operations and parse the JSON responses to dynamically update the page DOM."),
        ("15. CORS — @CrossOrigin (Cross-Origin Resource Sharing)",
         "I used the @CrossOrigin annotation on all my Spring REST controller classes. CORS is a browser security mechanism that blocks web pages from making requests to a different origin (protocol + host + port). By adding @CrossOrigin, Spring adds the Access-Control-Allow-Origin header to HTTP responses, allowing the browser to accept responses from the backend on port 8080."),
        ("16. @ControllerAdvice &amp; @ExceptionHandler (Global Exception Handling)",
         "I used Spring's @ControllerAdvice annotation to create a GlobalExceptionHandler class that intercepts exceptions thrown by any controller in the application. Instead of returning ugly stack traces or Whitelabel error pages, my handler catches RuntimeExceptions and returns clean JSON error responses with HTTP 400 (Bad Request) or HTTP 500 (Internal Server Error) status codes."),
        ("17. Dependency Injection &amp; IoC (Inversion of Control)",
         "I used Spring's Constructor-Based Dependency Injection throughout the application. Instead of creating objects with the 'new' keyword, Spring's IoC container automatically creates and injects dependencies. For example, BookService receives BookRepository via its constructor, and BookController receives BookService via its constructor. This promotes loose coupling and easy unit testing."),
        ("18. MultipartFile &amp; WebMvcConfigurer (File Upload &amp; Static Resource Serving)",
         "I used Spring's MultipartFile interface to handle binary image file uploads from the admin page. When an admin uploads a cover image, the file is received as a MultipartFile, saved to the local uploads/ directory with a unique timestamp prefix, and the public URL is returned. I also configured a WebMvcConfigurer bean to map /uploads/** HTTP requests to the physical uploads/ directory."),
        ("19. Apache Maven &amp; pom.xml (Build Tool &amp; Dependency Management)",
         "I used Apache Maven as the build automation tool. The pom.xml file declares all project dependencies (spring-boot-starter-data-jpa, spring-boot-starter-webmvc, mysql-connector-j, lombok). Maven downloads these JARs from Maven Central, compiles Java source code, runs tests, and packages the application into an executable JAR file."),
        ("20. Project Lombok (Boilerplate Code Reduction)",
         "I included Lombok in my pom.xml as an optional dependency. Lombok can auto-generate getter/setter methods, constructors, toString(), equals(), and hashCode() methods at compile time using annotations like @Getter, @Setter, @Data. In this project, I wrote getters/setters manually in the entities, but Lombok is configured and available for future use."),
    ]
    for title, desc in tech:
        S.append(Paragraph(f"<b>{title}</b>", h2))
        S.append(Paragraph(f"<i>\"{desc}\"</i>", cb_style))
        S.append(Spacer(1,2))

    S.append(PageBreak())

    # ═══════════════════════════════════════════════════════════════════════
    # SECTION 2: FILE STRUCTURE
    # ═══════════════════════════════════════════════════════════════════════
    S.append(Paragraph("Section 2 — Project File Structure &amp; What Each File Does", h1))
    S.append(Paragraph("Complete directory tree with the purpose and role of every single file:", b))
    S.append(Spacer(1,3))

    tree_code = (
        "bookstore/\n"
        "├── pom.xml                                          # Maven build config & dependencies\n"
        "├── src/main/resources/\n"
        "│   ├── application.properties                       # DB credentials, Hibernate, server port\n"
        "│   └── static/\n"
        "│       ├── index.html                               # Customer storefront (browse, cart, order)\n"
        "│       └── admin.html                               # Admin dashboard (add, delete, upload)\n"
        "├── src/main/java/com/bookhub/bookstore/\n"
        "│   ├── BookstoreApplication.java                    # Main entry point + uploads config\n"
        "│   ├── entity/\n"
        "│   │   ├── Book.java                                # @Entity -> `book` table\n"
        "│   │   ├── CartItem.java                            # @Entity -> `cart_item` table (FK to book)\n"
        "│   │   └── Order.java                               # @Entity -> `orders` table\n"
        "│   ├── dto/\n"
        "│   │   └── ApiResponse.java                         # Generic DTO: {success, message, data}\n"
        "│   ├── repository/\n"
        "│   │   ├── BookRepository.java                      # JpaRepository<Book, Long>\n"
        "│   │   ├── CartRepository.java                      # JpaRepository<CartItem, Long>\n"
        "│   │   └── OrderRepository.java                     # JpaRepository<Order, Long> + findByUserId\n"
        "│   ├── service/\n"
        "│   │   ├── BookService.java                         # CRUD logic for books\n"
        "│   │   ├── CartService.java                         # Add-to-cart with stock validation\n"
        "│   │   └── OrderService.java                        # Checkout: stock deduction, order creation\n"
        "│   ├── controller/\n"
        "│   │   ├── BookController.java                      # REST: /books endpoints + file upload\n"
        "│   │   ├── CartController.java                      # REST: /cart endpoints\n"
        "│   │   └── OrderController.java                     # REST: /orders endpoints\n"
        "│   └── exception/\n"
        "│       └── GlobalExceptionHandler.java              # @ControllerAdvice error handler\n"
        "└── uploads/                                         # Stored cover images (served via HTTP)"
    )
    S.append(cb(tree_code, cf))
    S.append(Spacer(1,4))

    file_table = [
        [Paragraph("<b>File</b>",h3), Paragraph("<b>Layer</b>",h3), Paragraph("<b>What It Does</b>",h3)],
        [Paragraph("pom.xml",bl), Paragraph("Build",bl), Paragraph("Declares dependencies (Spring Boot, JPA, MySQL driver, Lombok), Java 21 version, and Maven build plugins.",bl)],
        [Paragraph("application.properties",bl), Paragraph("Config",bl), Paragraph("Configures MySQL JDBC URL (localhost:3306/bookstore_db), username/password, Hibernate ddl-auto=update, show-sql=true, and server port 8080.",bl)],
        [Paragraph("BookstoreApplication.java",bl), Paragraph("Entry",bl), Paragraph("Contains main() which boots the Spring container. Also declares a @Bean WebMvcConfigurer to serve uploaded images from the uploads/ directory over HTTP.",bl)],
        [Paragraph("Book.java",bl), Paragraph("Entity",bl), Paragraph("JPA @Entity class mapping to the 'book' MySQL table. Fields: id (PK, auto-increment), title, author, price, quantity (stock), imageUrl.",bl)],
        [Paragraph("CartItem.java",bl), Paragraph("Entity",bl), Paragraph("JPA @Entity mapping to 'cart_item' table. Has a @ManyToOne relationship to Book via foreign key column 'book_id'. Fields: id, quantity, book.",bl)],
        [Paragraph("Order.java",bl), Paragraph("Entity",bl), Paragraph("JPA @Entity mapping to 'orders' table (not 'order' — SQL reserved word!). Fields: id, totalPrice, userId (non-nullable).",bl)],
        [Paragraph("ApiResponse.java",bl), Paragraph("DTO",bl), Paragraph("Generic wrapper class ApiResponse&lt;T&gt; with fields: boolean success, String message, T data. Returned by every controller endpoint.",bl)],
        [Paragraph("BookRepository.java",bl), Paragraph("Repository",bl), Paragraph("Interface extending JpaRepository&lt;Book, Long&gt;. Inherits findAll(), findById(), save(), deleteById() — zero SQL needed.",bl)],
        [Paragraph("CartRepository.java",bl), Paragraph("Repository",bl), Paragraph("Interface extending JpaRepository&lt;CartItem, Long&gt;. Uses findAll(), save(), deleteAll().",bl)],
        [Paragraph("OrderRepository.java",bl), Paragraph("Repository",bl), Paragraph("Extends JpaRepository&lt;Order, Long&gt;. Adds custom derived query method: List&lt;Order&gt; findByUserId(String userId) which auto-generates SELECT * FROM orders WHERE user_id = ?.",bl)],
        [Paragraph("BookService.java",bl), Paragraph("Service",bl), Paragraph("Business logic for catalog CRUD. Methods: getAllBooks(), saveBook(Book), deleteBook(Long id).",bl)],
        [Paragraph("CartService.java",bl), Paragraph("Service",bl), Paragraph("Validates book existence and stock availability before adding to cart. Methods: addToCart(id, qty), getCart(), clearCart().",bl)],
        [Paragraph("OrderService.java",bl), Paragraph("Service",bl), Paragraph("Orchestrates checkout: validates cart, checks stock, calculates total, decrements inventory, clears cart, saves order. Methods: placeOrder(userId), getOrdersByUser(userId).",bl)],
        [Paragraph("BookController.java",bl), Paragraph("Controller",bl), Paragraph("REST endpoints: GET /books, POST /books, DELETE /books/{id}, POST /books/upload. Maps HTTP requests to BookService methods.",bl)],
        [Paragraph("CartController.java",bl), Paragraph("Controller",bl), Paragraph("REST endpoints: POST /cart/{id}/{qty}, GET /cart. Maps to CartService methods.",bl)],
        [Paragraph("OrderController.java",bl), Paragraph("Controller",bl), Paragraph("REST endpoints: POST /orders/{userId}, GET /orders/{userId}. Maps to OrderService methods.",bl)],
        [Paragraph("GlobalExceptionHandler.java",bl), Paragraph("Exception",bl), Paragraph("@ControllerAdvice intercepting RuntimeException (HTTP 400) and Exception (HTTP 500) across all controllers.",bl)],
        [Paragraph("index.html",bl), Paragraph("Frontend",bl), Paragraph("Customer storefront. JS functions: loadBooks(), addToCart(), loadCart(), placeOrder(), loadOrders(), toggleCart(). Uses Fetch API.",bl)],
        [Paragraph("admin.html",bl), Paragraph("Frontend",bl), Paragraph("Admin dashboard. JS functions: addBook() (with image upload), loadBooks(), deleteBook(). Image preview via URL.createObjectURL().",bl)],
    ]
    ft = Table(file_table, colWidths=[110, 55, W-165])
    ft.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,0),colors.HexColor("#1d3557")),
        ('TEXTCOLOR',(0,0),(-1,0),colors.white),
        ('BOX',(0,0),(-1,-1),1,colors.HexColor("#cbd5e1")),
        ('INNERGRID',(0,0),(-1,-1),0.5,colors.HexColor("#e2e8f0")),
        ('LEFTPADDING',(0,0),(-1,-1),4),('RIGHTPADDING',(0,0),(-1,-1),4),
        ('TOPPADDING',(0,0),(-1,-1),3),('BOTTOMPADDING',(0,0),(-1,-1),3),
        ('VALIGN',(0,0),(-1,-1),'TOP'),
    ]))
    S.append(ft)
    S.append(PageBreak())

    # ═══════════════════════════════════════════════════════════════════════
    # SECTION 3: DATABASE ACCESS PIPELINE
    # ═══════════════════════════════════════════════════════════════════════
    S.append(Paragraph("Section 3 — How the Application Accesses MySQL (Complete Database Pipeline)", h1))
    S.append(Paragraph("This section explains, step by step, the entire chain from application.properties configuration down to raw SQL execution on MySQL:", b))
    S.append(Spacer(1,4))

    S.append(Paragraph("<b>Step 1: application.properties configures the DataSource</b>", h3))
    S.append(cb("spring.datasource.url=jdbc:mysql://localhost:3306/bookstore_db\nspring.datasource.username=root\nspring.datasource.password=root", cf))
    S.append(Paragraph("At startup, Spring Boot reads these properties and creates a <code>HikariDataSource</code> bean. HikariCP uses <code>mysql-connector-j</code> (the JDBC driver) to open real TCP socket connections to the MySQL server process listening on <code>localhost:3306</code>.", bl))
    S.append(Spacer(1,3))

    S.append(Paragraph("<b>Step 2: Hibernate scans @Entity classes and creates/updates tables (ddl-auto=update)</b>", h3))
    S.append(Paragraph("Hibernate inspects <code>Book.java</code>, <code>CartItem.java</code>, and <code>Order.java</code>. For each @Entity, it checks if the corresponding MySQL table exists. If not, it executes CREATE TABLE. If the table exists but columns differ, it executes ALTER TABLE. This is controlled by <code>spring.jpa.hibernate.ddl-auto=update</code>.", bl))
    S.append(cb("-- Hibernate auto-generated DDL:\nCREATE TABLE book (id BIGINT AUTO_INCREMENT PRIMARY KEY, title VARCHAR(255), author VARCHAR(255), price DOUBLE, quantity INT, image_url VARCHAR(255));\nCREATE TABLE cart_item (id BIGINT AUTO_INCREMENT PRIMARY KEY, quantity INT, book_id BIGINT, FOREIGN KEY (book_id) REFERENCES book(id));\nCREATE TABLE orders (id BIGINT AUTO_INCREMENT PRIMARY KEY, total_price DOUBLE, user_id VARCHAR(255) NOT NULL);", cf))
    S.append(Spacer(1,3))

    S.append(Paragraph("<b>Step 3: Spring Data JPA generates Repository proxy implementations</b>", h3))
    S.append(Paragraph("Spring scans interfaces like <code>BookRepository extends JpaRepository&lt;Book, Long&gt;</code>. At runtime, Spring creates a dynamic proxy class (backed by <code>SimpleJpaRepository</code>) that implements all CRUD methods. No developer implementation class is needed!", bl))
    S.append(Spacer(1,3))

    S.append(Paragraph("<b>Step 4: Query execution lifecycle (what happens when code calls repo.findAll())</b>", h3))
    flow_lines = [
        "Java Code:  bookRepo.findAll()",
        "    |",
        "    v",
        "Spring Data JPA proxy -> Hibernate EntityManager",
        "    |",
        "    v",
        "Hibernate generates SQL: SELECT b.id, b.title, b.author, b.price, b.quantity, b.image_url FROM book b",
        "    |",
        "    v",
        "HikariCP borrows a pooled JDBC Connection (TCP socket to MySQL)",
        "    |",
        "    v",
        "MySQL server executes query, returns ResultSet over TCP",
        "    |",
        "    v",
        "Hibernate maps ResultSet rows -> List<Book> Java objects",
        "    |",
        "    v",
        "HikariCP returns Connection to pool (reused for next request)",
        "    |",
        "    v",
        "Service returns List<Book> -> Controller wraps in ApiResponse -> Jackson serializes to JSON"
    ]
    S.append(flow_box(flow_lines, cf))
    S.append(Spacer(1,3))

    S.append(Paragraph("<b>Step 5: Derived Query Methods (how findByUserId works)</b>", h3))
    S.append(cb("// In OrderRepository.java:\nList<Order> findByUserId(String userId);\n\n// Spring Data JPA parses the method name:\n//   findBy  -> SELECT * FROM orders WHERE\n//   UserId  -> user_id = ?\n// Auto-generated SQL: SELECT * FROM orders WHERE user_id = ?", cf))
    S.append(Paragraph("Spring Data JPA analyzes the method name at startup. It splits <code>findByUserId</code> into <code>findBy</code> (query keyword) + <code>UserId</code> (property name on the Order entity). It then generates the SQL query automatically. No JPQL, no native SQL, no manual implementation!", bl))
    S.append(Spacer(1,3))

    S.append(callout(
        "<b>Interview Summary:</b> 'My application accesses MySQL through a 5-layer pipeline: "
        "<b>application.properties</b> configures the JDBC URL and credentials &rarr; "
        "<b>HikariCP</b> maintains a pool of TCP connections to MySQL &rarr; "
        "<b>Hibernate ORM</b> maps Java entities to SQL tables and auto-generates DDL &rarr; "
        "<b>Spring Data JPA</b> creates dynamic proxy implementations of my Repository interfaces &rarr; "
        "When my code calls methods like <code>findAll()</code> or <code>save()</code>, Hibernate generates the SQL query, borrows a HikariCP connection, executes the query on MySQL, maps the results back to Java objects, and returns the connection to the pool.'",
        cb_style, title="MEMORIZE THIS FOR YOUR INTERVIEW", bg="#f0fdf4", border="#16a34a"
    ))
    S.append(PageBreak())

    # ═══════════════════════════════════════════════════════════════════════
    # SECTION 4: FRONTEND-BACKEND CONNECTION
    # ═══════════════════════════════════════════════════════════════════════
    S.append(Paragraph("Section 4 — How Frontend Connects to Backend (Complete HTTP Lifecycle)", h1))
    S.append(Paragraph("This is <b>the most important answer</b> for your interview. Understand every step of how a button click in HTML reaches MySQL and returns data:", b))
    S.append(Spacer(1,4))

    S.append(Paragraph("<b>Complete Request-Response Lifecycle (every single step):</b>", h3))
    lifecycle = [
        "1. USER clicks 'Add to Cart' button in index.html",
        "2. JavaScript function addToCart(id, stock) is invoked",
        "3. Client-side validation: checks qty > 0 and qty <= stock",
        "4. Browser executes: fetch('http://localhost:8080/cart/1/2', { method: 'POST' })",
        "5. Browser creates HTTP POST request with headers and sends over TCP to localhost:8080",
        "6. Embedded Tomcat receives the TCP connection and HTTP request",
        "7. Tomcat passes request to Spring DispatcherServlet",
        "8. DispatcherServlet consults HandlerMapping to find matching @RequestMapping",
        "9. Finds: CartController.add(@PathVariable Long id, @PathVariable int qty)",
        "10. Spring extracts path variables: id=1, qty=2 from URL /cart/1/2",
        "11. CartController.add() calls CartService.addToCart(1, 2)",
        "12. CartService calls bookRepo.findById(1L)",
        "13. Spring Data JPA proxy -> Hibernate -> SQL: SELECT * FROM book WHERE id = 1",
        "14. HikariCP borrows connection -> MySQL executes query -> returns ResultSet",
        "15. Hibernate maps row to Book Java object",
        "16. CartService validates: qty(2) <= book.getQuantity(10)? YES -> continues",
        "17. CartService creates new CartItem, sets book and quantity",
        "18. CartService calls cartRepo.save(item)",
        "19. Hibernate -> SQL: INSERT INTO cart_item (book_id, quantity) VALUES (1, 2)",
        "20. MySQL inserts row, returns generated ID",
        "21. CartService returns CartItem to CartController",
        "22. CartController wraps in: new ApiResponse<>(true, 'Added', cartItem)",
        "23. Jackson ObjectMapper serializes ApiResponse to JSON string",
        "24. Spring sets Content-Type: application/json, @CrossOrigin adds CORS headers",
        "25. Tomcat sends HTTP 200 OK response with JSON body back to browser",
        "26. Browser's fetch() Promise resolves with the Response object",
        "27. JavaScript calls res.json() to parse JSON response",
        "28. JavaScript displays alert('Added 2 x \"Clean Code\" to your cart!')",
        "29. JavaScript calls loadBooks() and loadCart() to refresh the UI",
    ]
    S.append(flow_box(lifecycle, cf, bg="#f0f9ff", border="#0284c7"))
    S.append(Spacer(1,4))

    S.append(callout(
        "<b>Interview Answer (memorize this):</b> "
        "'I connect the HTML/JS frontend and Spring Boot backend through REST APIs. "
        "The frontend uses the native JavaScript Fetch API to send HTTP requests (GET, POST, DELETE) "
        "to endpoints like /books, /cart/{id}/{qty}, and /orders/{userId}. "
        "The Spring Boot backend uses @RestController classes with @GetMapping, @PostMapping, and @DeleteMapping "
        "to receive requests. The controller delegates to a @Service class for business logic, "
        "which calls @Repository interfaces for database access via Spring Data JPA and Hibernate. "
        "All responses are wrapped in a standardized ApiResponse&lt;T&gt; DTO and serialized to JSON by Jackson. "
        "@CrossOrigin enables CORS so the browser accepts responses from the backend.'",
        cb_style, title="FRONTEND-BACKEND CONNECTION — MEMORIZE THIS", bg="#fef3c7", border="#d97706"
    ))
    S.append(PageBreak())

    # ═══════════════════════════════════════════════════════════════════════
    # SECTION 5: EVERY FILE, EVERY FUNCTION, WITH FULL CODE
    # ═══════════════════════════════════════════════════════════════════════
    S.append(Paragraph("Section 5 — File-by-File &amp; Function-by-Function Code Breakdown", h1))
    S.append(Paragraph("Every single file, every function, with the actual code and line-by-line explanation:", b))
    S.append(Spacer(1,4))

    # --- 5.1 application.properties ---
    S.append(Paragraph("<b>FILE 1: application.properties</b> (src/main/resources/)", h2))
    S.append(Paragraph("<b>What it does:</b> Central configuration file read by Spring Boot at startup. No Java code — just key-value pairs.", b))
    S.append(cb(
        "spring.datasource.url=jdbc:mysql://localhost:3306/bookstore_db   # JDBC URL: protocol:subprotocol://host:port/database\n"
        "spring.datasource.username=root                                   # MySQL login username\n"
        "spring.datasource.password=root                                   # MySQL login password\n"
        "spring.jpa.open-in-view=false          # Closes DB connections after service layer (prevents connection leaks)\n"
        "spring.jpa.hibernate.ddl-auto=update   # Hibernate auto-creates/updates tables from @Entity classes\n"
        "spring.jpa.show-sql=true               # Prints all Hibernate-generated SQL to console for debugging\n"
        "server.port=8080                        # Embedded Tomcat listens on this TCP port", cf))
    S.append(Spacer(1,6))

    # --- 5.2 BookstoreApplication.java ---
    S.append(Paragraph("<b>FILE 2: BookstoreApplication.java</b>", h2))
    S.append(Paragraph("<b>What it does:</b> The main() entry point that boots the entire application, and configures static resource serving for uploaded images.", b))
    S.append(cb(
        "@SpringBootApplication  // = @Configuration + @EnableAutoConfiguration + @ComponentScan\n"
        "public class BookstoreApplication {\n\n"
        "    // FUNCTION: main(String[] args)\n"
        "    // WHAT: The very first line executed by the JVM. Bootstraps Spring Boot.\n"
        "    // HOW: SpringApplication.run() creates ApplicationContext, performs component scanning,\n"
        "    //      auto-configures DataSource/Hibernate/Tomcat, and starts listening on port 8080.\n"
        "    public static void main(String[] args) {\n"
        "        SpringApplication.run(BookstoreApplication.class, args);\n"
        "    }\n\n"
        "    // FUNCTION: config()\n"
        "    // WHAT: Returns a WebMvcConfigurer bean that maps HTTP /uploads/** to file:uploads/\n"
        "    // WHY: By default Spring only serves from src/main/resources/static. This makes the\n"
        "    //      external uploads/ directory publicly accessible so cover images load in browsers.\n"
        "    // EXAMPLE: uploads/1740000000_cover.jpg -> http://localhost:8080/uploads/1740000000_cover.jpg\n"
        "    @Bean\n"
        "    public WebMvcConfigurer config() {\n"
        "        return new WebMvcConfigurer() {\n"
        "            @Override\n"
        "            public void addResourceHandlers(ResourceHandlerRegistry registry) {\n"
        "                registry.addResourceHandler(\"/uploads/**\")\n"
        "                        .addResourceLocations(\"file:uploads/\");\n"
        "            }\n"
        "        };\n"
        "    }\n"
        "}", cf))
    S.append(Spacer(1,6))

    # --- 5.3-5.5 Entities ---
    S.append(Paragraph("<b>FILE 3: Book.java</b> (entity package)", h2))
    S.append(Paragraph("<b>What it does:</b> Defines the Book database table schema in Java. Each instance = one row in the 'book' MySQL table.", b))
    S.append(cb(
        "@Entity  // Tells Hibernate: this class maps to a database table\n"
        "public class Book {\n\n"
        "    @Id                                      // This field is the Primary Key\n"
        "    @GeneratedValue(strategy = GenerationType.IDENTITY)  // MySQL AUTO_INCREMENT\n"
        "    private Long id;     // PK, auto-generated. SQL: id BIGINT AUTO_INCREMENT PRIMARY KEY\n\n"
        "    private String title;    // Book title.    SQL: title VARCHAR(255)\n"
        "    private String author;   // Author name.   SQL: author VARCHAR(255)\n"
        "    private double price;    // Price in Rs.   SQL: price DOUBLE\n"
        "    private int quantity;    // Warehouse stock. SQL: quantity INT\n"
        "    private String imageUrl; // Cover image URL. SQL: image_url VARCHAR(255)\n\n"
        "    public Book() {}  // Required by JPA for reflection-based instantiation\n\n"
        "    // Getter methods: getId(), getTitle(), getAuthor(), getPrice(), getQuantity(), getImageUrl()\n"
        "    //   -> Used by Jackson to serialize field values into JSON keys\n"
        "    //   -> Used by Hibernate to read field values for SQL queries\n\n"
        "    // Setter methods: setId(), setTitle(), setAuthor(), setPrice(), setQuantity(), setImageUrl()\n"
        "    //   -> Used by Jackson to deserialize JSON into object fields\n"
        "    //   -> Used by Hibernate to populate fields from ResultSet data\n"
        "    //   -> Used by OrderService to decrement stock: book.setQuantity(stock - qty)\n"
        "}", cf))
    S.append(Spacer(1,4))

    S.append(Paragraph("<b>FILE 4: CartItem.java</b> (entity package)", h2))
    S.append(Paragraph("<b>What it does:</b> Represents one item in the shopping cart. Links to Book via a foreign key relationship.", b))
    S.append(cb(
        "@Entity  // Maps to 'cart_item' table\n"
        "public class CartItem {\n\n"
        "    @Id @GeneratedValue(strategy = GenerationType.IDENTITY)\n"
        "    private Long id;\n\n"
        "    private int quantity;  // How many copies of this book the customer wants\n\n"
        "    @ManyToOne                     // Relationship: Many CartItems can reference One Book\n"
        "    @JoinColumn(name = \"book_id\")  // Creates FK column 'book_id' in cart_item table\n"
        "    private Book book;             // Hibernate auto-JOINs: cartItem.getBook().getTitle()\n\n"
        "    public CartItem() {}  // Required by JPA\n"
        "    // Getters: getId(), getQuantity(), getBook()\n"
        "    // Setters: setId(), setQuantity(), setBook()\n"
        "}", cf))
    S.append(Spacer(1,4))

    S.append(Paragraph("<b>FILE 5: Order.java</b> (entity package)", h2))
    S.append(Paragraph("<b>What it does:</b> Stores permanent transaction records after checkout. Note the @Table(name='orders') to avoid SQL reserved word conflict.", b))
    S.append(cb(
        "@Entity\n"
        "@Table(name = \"orders\")  // CRITICAL: 'order' is SQL reserved keyword (used in ORDER BY)\n"
        "                          // Without this, Hibernate would generate: CREATE TABLE order ...\n"
        "                          // which causes a MySQL syntax error!\n"
        "public class Order {\n\n"
        "    @Id @GeneratedValue(strategy = GenerationType.IDENTITY)\n"
        "    private Long id;\n\n"
        "    private double totalPrice;  // Sum of (qty * price) for all cart items at checkout\n\n"
        "    @Column(nullable = false)   // Adds NOT NULL constraint in MySQL\n"
        "    private String userId;      // Which customer placed this order (e.g., \"user1\")\n\n"
        "    public Order() {}\n"
        "    // Getters and Setters\n"
        "}", cf))
    S.append(Spacer(1,6))

    # --- 5.6 ApiResponse ---
    S.append(Paragraph("<b>FILE 6: ApiResponse.java</b> (dto package)", h2))
    S.append(Paragraph("<b>What it does:</b> Generic wrapper ensuring ALL endpoints return a consistent JSON structure.", b))
    S.append(cb(
        "public class ApiResponse<T> {\n\n"
        "    private boolean success;  // true = operation worked, false = error occurred\n"
        "    private String message;   // Human-readable status (\"Books fetched\", \"Stock not available\")\n"
        "    private T data;           // The actual payload: List<Book>, Book, CartItem, Order, or null\n\n"
        "    public ApiResponse() {}   // Jackson needs this for deserialization\n\n"
        "    // Constructor used by every controller:\n"
        "    public ApiResponse(boolean success, String message, T data) {\n"
        "        this.success = success;\n"
        "        this.message = message;\n"
        "        this.data = data;\n"
        "    }\n\n"
        "    // Getters (isSuccess(), getMessage(), getData()) -> Jackson reads these to create JSON keys\n"
        "    // Setters (setSuccess(), setMessage(), setData())\n"
        "}\n\n"
        "// EXAMPLE JSON OUTPUT:\n"
        "// { \"success\": true, \"message\": \"Books fetched\", \"data\": [{\"id\":1,\"title\":\"Clean Code\",...}] }", cf))
    S.append(Spacer(1,6))

    # --- 5.7-5.9 Repositories ---
    S.append(Paragraph("<b>FILES 7-9: Repository Interfaces</b> (repository package)", h2))
    S.append(Paragraph("<b>What they do:</b> Define the data access layer. Spring auto-generates implementations at runtime.", b))
    S.append(cb(
        "// BookRepository.java\n"
        "public interface BookRepository extends JpaRepository<Book, Long> {\n"
        "    // INHERITS (no code needed!):\n"
        "    // List<Book> findAll()           -> SELECT * FROM book\n"
        "    // Optional<Book> findById(Long)  -> SELECT * FROM book WHERE id = ?\n"
        "    // Book save(Book book)           -> INSERT INTO book ... (if new) or UPDATE book ... (if existing)\n"
        "    // void deleteById(Long id)       -> DELETE FROM book WHERE id = ?\n"
        "}\n\n"
        "// CartRepository.java\n"
        "public interface CartRepository extends JpaRepository<CartItem, Long> {\n"
        "    // INHERITS:\n"
        "    // List<CartItem> findAll()  -> SELECT * FROM cart_item (with eager fetch of Book)\n"
        "    // CartItem save(CartItem)   -> INSERT INTO cart_item ...\n"
        "    // void deleteAll()          -> DELETE FROM cart_item  (clears entire cart)\n"
        "}\n\n"
        "// OrderRepository.java\n"
        "public interface OrderRepository extends JpaRepository<Order, Long> {\n\n"
        "    // CUSTOM DERIVED QUERY METHOD:\n"
        "    List<Order> findByUserId(String userId);\n"
        "    // Spring parses method name: findBy + UserId\n"
        "    // Auto-generates: SELECT * FROM orders WHERE user_id = ?\n"
        "    // No SQL, no JPQL, no @Query annotation needed!\n"
        "}", cf))
    S.append(Spacer(1,6))

    # --- 5.10 BookService ---
    S.append(Paragraph("<b>FILE 10: BookService.java</b> (service package)", h2))
    S.append(Paragraph("<b>What it does:</b> Contains business logic for book catalog management. Injected into BookController.", b))
    S.append(cb(
        "@Service  // Marks this as a Spring-managed service bean\n"
        "public class BookService {\n\n"
        "    private final BookRepository repo;  // Injected by Spring\n\n"
        "    // Constructor Injection: Spring provides BookRepository when creating this bean\n"
        "    public BookService(BookRepository repo) {\n"
        "        this.repo = repo;\n"
        "    }\n\n"
        "    // FUNCTION: getAllBooks()\n"
        "    // WHAT: Returns every book in the catalog\n"
        "    // SQL: SELECT * FROM book\n"
        "    public List<Book> getAllBooks() {\n"
        "        return repo.findAll();\n"
        "    }\n\n"
        "    // FUNCTION: saveBook(Book book)\n"
        "    // WHAT: Inserts a new book or updates an existing one\n"
        "    // SQL: INSERT INTO book (...) VALUES (...) [if id is null]\n"
        "    //      UPDATE book SET ... WHERE id = ?    [if id exists]\n"
        "    public Book saveBook(Book book) {\n"
        "        return repo.save(book);\n"
        "    }\n\n"
        "    // FUNCTION: deleteBook(Long id)\n"
        "    // WHAT: Removes a book from catalog\n"
        "    // SQL: DELETE FROM book WHERE id = ?\n"
        "    public void deleteBook(Long id) {\n"
        "        repo.deleteById(id);\n"
        "    }\n"
        "}", cf))
    S.append(Spacer(1,6))

    # --- 5.11 CartService ---
    S.append(Paragraph("<b>FILE 11: CartService.java</b> (service package)", h2))
    S.append(Paragraph("<b>What it does:</b> Validates book existence and stock availability, then saves cart items. Contains critical business rules.", b))
    S.append(cb(
        "@Service\n"
        "public class CartService {\n\n"
        "    private final CartRepository cartRepo;\n"
        "    private final BookRepository bookRepo;\n\n"
        "    public CartService(CartRepository cartRepo, BookRepository bookRepo) {\n"
        "        this.cartRepo = cartRepo;\n"
        "        this.bookRepo = bookRepo;\n"
        "    }\n\n"
        "    // FUNCTION: addToCart(Long id, int qty)\n"
        "    // WHAT: Validates and adds a book to the cart\n"
        "    // STEP 1: Look up book by ID. If not found -> throw RuntimeException\n"
        "    // STEP 2: Check if qty exceeds warehouse stock. If yes -> throw RuntimeException\n"
        "    // STEP 3: Create CartItem, link to Book, save to MySQL\n"
        "    public CartItem addToCart(Long id, int qty) {\n"
        "        Book book = bookRepo.findById(id)                          // SQL: SELECT * FROM book WHERE id = ?\n"
        "                .orElseThrow(() -> new RuntimeException(\"Book not found\"));  // -> HTTP 400\n\n"
        "        if (qty > book.getQuantity()) {                            // Business rule: can't exceed stock\n"
        "            throw new RuntimeException(\"Stock not available\");     // -> HTTP 400\n"
        "        }\n\n"
        "        CartItem item = new CartItem();\n"
        "        item.setBook(book);       // Sets foreign key book_id\n"
        "        item.setQuantity(qty);\n"
        "        return cartRepo.save(item);  // SQL: INSERT INTO cart_item (book_id, quantity) VALUES (?, ?)\n"
        "    }\n\n"
        "    // FUNCTION: getCart()\n"
        "    // SQL: SELECT * FROM cart_item JOIN book ON cart_item.book_id = book.id\n"
        "    public List<CartItem> getCart() {\n"
        "        return cartRepo.findAll();\n"
        "    }\n\n"
        "    // FUNCTION: clearCart()\n"
        "    // SQL: DELETE FROM cart_item\n"
        "    public void clearCart() {\n"
        "        cartRepo.deleteAll();\n"
        "    }\n"
        "}", cf))
    S.append(Spacer(1,6))

    # --- 5.12 OrderService ---
    S.append(Paragraph("<b>FILE 12: OrderService.java</b> (service package) — THE MOST COMPLEX SERVICE", h2))
    S.append(Paragraph("<b>What it does:</b> Orchestrates the entire checkout workflow: validates cart, re-checks stock, calculates total, decrements inventory, clears cart, and creates the order record.", b))
    S.append(cb(
        "@Service\n"
        "public class OrderService {\n\n"
        "    private final CartRepository cartRepo;\n"
        "    private final BookRepository bookRepo;\n"
        "    private final OrderRepository orderRepo;\n\n"
        "    public OrderService(CartRepository cartRepo, BookRepository bookRepo, OrderRepository orderRepo) {\n"
        "        this.cartRepo = cartRepo;\n"
        "        this.bookRepo = bookRepo;\n"
        "        this.orderRepo = orderRepo;\n"
        "    }\n\n"
        "    // FUNCTION: placeOrder(String userId)\n"
        "    // THE MOST IMPORTANT FUNCTION IN THE ENTIRE APPLICATION\n"
        "    // STEP 1: Fetch all cart items (SQL: SELECT * FROM cart_item)\n"
        "    // STEP 2: If cart empty -> throw RuntimeException -> HTTP 400\n"
        "    // STEP 3: Loop through each CartItem:\n"
        "    //   a) Get the associated Book\n"
        "    //   b) Verify stock hasn't been depleted since adding to cart\n"
        "    //   c) Accumulate total price: total += qty * price\n"
        "    //   d) Deduct stock: book.setQuantity(stock - qty)\n"
        "    //   e) Save updated book (SQL: UPDATE book SET quantity = ? WHERE id = ?)\n"
        "    // STEP 4: Clear cart (SQL: DELETE FROM cart_item)\n"
        "    // STEP 5: Create Order with totalPrice and userId\n"
        "    // STEP 6: Save order (SQL: INSERT INTO orders (total_price, user_id) VALUES (?, ?))\n"
        "    public Order placeOrder(String userId) {\n"
        "        List<CartItem> items = cartRepo.findAll();   // STEP 1\n"
        "        if (items.isEmpty()) {                       // STEP 2\n"
        "            throw new RuntimeException(\"Cart is empty\");\n"
        "        }\n"
        "        double total = 0;\n"
        "        for (CartItem item : items) {                // STEP 3\n"
        "            Book book = item.getBook();\n"
        "            if (item.getQuantity() > book.getQuantity()) {\n"
        "                throw new RuntimeException(\"Stock not available\");\n"
        "            }\n"
        "            total += item.getQuantity() * book.getPrice();           // 3c\n"
        "            book.setQuantity(book.getQuantity() - item.getQuantity()); // 3d\n"
        "            bookRepo.save(book);                                      // 3e\n"
        "        }\n"
        "        cartRepo.deleteAll();                        // STEP 4\n"
        "        Order order = new Order();                   // STEP 5\n"
        "        order.setTotalPrice(total);\n"
        "        order.setUserId(userId);\n"
        "        return orderRepo.save(order);                // STEP 6\n"
        "    }\n\n"
        "    // FUNCTION: getOrdersByUser(String userId)\n"
        "    // SQL: SELECT * FROM orders WHERE user_id = ?\n"
        "    public List<Order> getOrdersByUser(String userId) {\n"
        "        return orderRepo.findByUserId(userId);\n"
        "    }\n"
        "}", cf))
    S.append(Spacer(1,6))

    # --- 5.13-5.15 Controllers ---
    S.append(Paragraph("<b>FILE 13: BookController.java</b> (controller package)", h2))
    S.append(Paragraph("<b>What it does:</b> Exposes REST HTTP endpoints for book catalog management. Maps URLs to service methods.", b))
    S.append(cb(
        "@RestController          // = @Controller + @ResponseBody (returns JSON, not HTML views)\n"
        "@RequestMapping(\"/books\") // Base URL prefix: all endpoints start with /books\n"
        "@CrossOrigin             // Adds CORS headers so browsers allow cross-origin requests\n"
        "public class BookController {\n\n"
        "    private final BookService service;\n"
        "    public BookController(BookService service) { this.service = service; }\n\n"
        "    // ENDPOINT: GET /books\n"
        "    // WHAT: Returns all books in the catalog\n"
        "    // CALLED BY: index.html loadBooks(), admin.html loadBooks()\n"
        "    @GetMapping\n"
        "    public ApiResponse<List<Book>> getBooks() {\n"
        "        return new ApiResponse<>(true, \"Books fetched\", service.getAllBooks());\n"
        "    }\n\n"
        "    // ENDPOINT: POST /books\n"
        "    // WHAT: Adds a new book. @RequestBody deserializes JSON body into Book object.\n"
        "    // CALLED BY: admin.html addBook()\n"
        "    @PostMapping\n"
        "    public ApiResponse<Book> addBook(@RequestBody Book book) {\n"
        "        return new ApiResponse<>(true, \"Book added\", service.saveBook(book));\n"
        "    }\n\n"
        "    // ENDPOINT: DELETE /books/{id}\n"
        "    // WHAT: Deletes book by ID. @PathVariable extracts 'id' from URL.\n"
        "    // CALLED BY: admin.html deleteBook(id)\n"
        "    @DeleteMapping(\"/{id}\")\n"
        "    public ApiResponse<String> deleteBook(@PathVariable Long id) {\n"
        "        service.deleteBook(id);\n"
        "        return new ApiResponse<>(true, \"Book deleted\", null);\n"
        "    }\n\n"
        "    // ENDPOINT: POST /books/upload\n"
        "    // WHAT: Receives binary image file, saves to uploads/ with timestamp prefix\n"
        "    // CALLED BY: admin.html addBook() (Step 1 of 2)\n"
        "    @PostMapping(\"/upload\")\n"
        "    public String uploadImage(@RequestParam(\"file\") MultipartFile file) throws Exception {\n"
        "        String folder = \"uploads/\";\n"
        "        File dir = new File(folder);\n"
        "        if (!dir.exists()) dir.mkdirs();                            // Create directory if missing\n"
        "        String fileName = System.currentTimeMillis() + \"_\" + file.getOriginalFilename();\n"
        "        String path = folder + fileName;\n"
        "        file.transferTo(new File(path));                            // Write bytes to disk\n"
        "        return \"http://localhost:8080/\" + path;                     // Return public URL\n"
        "    }\n"
        "}", cf))
    S.append(Spacer(1,4))

    S.append(Paragraph("<b>FILE 14: CartController.java</b> (controller package)", h2))
    S.append(cb(
        "@RestController\n"
        "@RequestMapping(\"/cart\")\n"
        "@CrossOrigin\n"
        "public class CartController {\n\n"
        "    private final CartService service;\n"
        "    public CartController(CartService service) { this.service = service; }\n\n"
        "    // ENDPOINT: POST /cart/{id}/{qty}\n"
        "    // WHAT: Adds book to cart. Both id and qty come from URL path.\n"
        "    // CALLED BY: index.html addToCart(id, stock)\n"
        "    @PostMapping(\"/{id}/{qty}\")\n"
        "    public ApiResponse<CartItem> add(@PathVariable Long id, @PathVariable int qty) {\n"
        "        return new ApiResponse<>(true, \"Added\", service.addToCart(id, qty));\n"
        "    }\n\n"
        "    // ENDPOINT: GET /cart\n"
        "    // WHAT: Returns all current cart items with nested Book data\n"
        "    // CALLED BY: index.html loadBooks() and loadCart()\n"
        "    @GetMapping\n"
        "    public List<CartItem> get() {\n"
        "        return service.getCart();\n"
        "    }\n"
        "}", cf))
    S.append(Spacer(1,4))

    S.append(Paragraph("<b>FILE 15: OrderController.java</b> (controller package)", h2))
    S.append(cb(
        "@RestController\n"
        "@RequestMapping(\"/orders\")\n"
        "@CrossOrigin\n"
        "public class OrderController {\n\n"
        "    private final OrderService service;\n"
        "    public OrderController(OrderService service) { this.service = service; }\n\n"
        "    // ENDPOINT: POST /orders/{userId}\n"
        "    // WHAT: Places order for given user. Triggers checkout workflow.\n"
        "    // CALLED BY: index.html placeOrder()\n"
        "    @PostMapping(\"/{userId}\")\n"
        "    public ApiResponse<Order> placeOrder(@PathVariable String userId) {\n"
        "        return new ApiResponse<>(true, \"Order placed\", service.placeOrder(userId));\n"
        "    }\n\n"
        "    // ENDPOINT: GET /orders/{userId}\n"
        "    // WHAT: Fetches order history for given user.\n"
        "    // CALLED BY: index.html loadOrders()\n"
        "    @GetMapping(\"/{userId}\")\n"
        "    public ApiResponse<List<Order>> getOrders(@PathVariable String userId) {\n"
        "        return new ApiResponse<>(true, \"Orders fetched\", service.getOrdersByUser(userId));\n"
        "    }\n"
        "}", cf))
    S.append(Spacer(1,6))

    # --- 5.16 GlobalExceptionHandler ---
    S.append(Paragraph("<b>FILE 16: GlobalExceptionHandler.java</b> (exception package)", h2))
    S.append(Paragraph("<b>What it does:</b> Intercepts all unhandled exceptions across every controller and converts them into clean JSON error responses.", b))
    S.append(cb(
        "@ControllerAdvice  // AOP: applies to ALL @RestController classes automatically\n"
        "public class GlobalExceptionHandler {\n\n"
        "    // FUNCTION: handleRuntimeException(RuntimeException ex)\n"
        "    // CATCHES: \"Book not found\", \"Stock not available\", \"Cart is empty\"\n"
        "    // RETURNS: HTTP 400 Bad Request + ApiResponse(false, ex.getMessage(), null)\n"
        "    @ExceptionHandler(RuntimeException.class)\n"
        "    public ResponseEntity<ApiResponse<Object>> handleRuntimeException(RuntimeException ex) {\n"
        "        ApiResponse<Object> response = new ApiResponse<>(false, ex.getMessage(), null);\n"
        "        return new ResponseEntity<>(response, HttpStatus.BAD_REQUEST);  // 400\n"
        "    }\n\n"
        "    // FUNCTION: handleGeneralException(Exception ex)\n"
        "    // CATCHES: Any unexpected error (NullPointerException, DB connection failure, etc.)\n"
        "    // RETURNS: HTTP 500 Internal Server Error + generic safe message\n"
        "    @ExceptionHandler(Exception.class)\n"
        "    public ResponseEntity<ApiResponse<Object>> handleGeneralException(Exception ex) {\n"
        "        ApiResponse<Object> response = new ApiResponse<>(false, \"Something went wrong\", null);\n"
        "        return new ResponseEntity<>(response, HttpStatus.INTERNAL_SERVER_ERROR);  // 500\n"
        "    }\n"
        "}", cf))
    S.append(Spacer(1,6))

    # --- 5.17-5.18 Frontend ---
    S.append(Paragraph("<b>FILE 17: index.html</b> (Customer Storefront) — All JavaScript Functions", h2))
    S.append(Paragraph("<b>What it does:</b> Single-page customer interface for browsing books, managing cart, placing orders, and viewing order history. Uses Fetch API.", b))
    S.append(cb(
        "// GLOBAL VARIABLE:\n"
        "const userId = \"user1\";  // Hardcoded user ID (in production: from JWT/session)\n\n"
        "// FUNCTION 1: loadBooks()\n"
        "// WHAT: Fetches book catalog AND cart items, merges them, renders HTML cards\n"
        "// HTTP: GET /books + GET /cart (parallel requests)\n"
        "async function loadBooks() {\n"
        "    let res = await fetch('http://localhost:8080/books');         // GET all books\n"
        "    let data = await res.json();                                  // Parse ApiResponse\n"
        "    let cartRes = await fetch('http://localhost:8080/cart');       // GET cart items\n"
        "    let cart = await cartRes.json();\n"
        "    let cartMap = {};\n"
        "    cart.forEach(c => { cartMap[c.book.id] = c.quantity; });\n"
        "    data.data.forEach(b => {\n"
        "        let cartQty = cartMap[b.id] || 0;  // How many already in cart\n"
        "        // Renders: image, title, author, price, stock, 'In Cart: X', qty input, Add button\n"
        "    });\n"
        "    document.getElementById('books').innerHTML = html;\n"
        "}\n\n"
        "// FUNCTION 2: addToCart(id, stock)\n"
        "// WHAT: Validates input, sends POST to add item to cart, refreshes UI\n"
        "// HTTP: POST /cart/{id}/{qty}\n"
        "async function addToCart(id, stock) {\n"
        "    let qty = parseInt(document.getElementById('qty-' + id).value);\n"
        "    if (!qty || qty <= 0) return alert('Enter valid quantity');\n"
        "    if (qty > stock) return alert('Exceeds stock!');\n"
        "    let res = await fetch(`http://localhost:8080/cart/${id}/${qty}`, { method: 'POST' });\n"
        "    let result = await res.json();\n"
        "    if (res.ok) { alert('Added!'); loadBooks(); loadCart(); }\n"
        "    else { alert('Error: ' + result.message); }\n"
        "}\n\n"
        "// FUNCTION 3: loadCart()\n"
        "// WHAT: Fetches cart items, calculates total, updates cart drawer + badge\n"
        "// HTTP: GET /cart\n"
        "async function loadCart() {\n"
        "    let res = await fetch('http://localhost:8080/cart');\n"
        "    let cart = await res.json();\n"
        "    let total = 0, count = 0;\n"
        "    cart.forEach(item => {\n"
        "        total += item.book.price * item.quantity;\n"
        "        count += item.quantity;\n"
        "    });\n"
        "    document.getElementById('cart').innerHTML = html;\n"
        "    document.getElementById('total').innerText = 'Total: Rs' + total;\n"
        "    document.getElementById('cartCount').innerText = count;\n"
        "}", cf))
    S.append(Spacer(1,4))

    S.append(Paragraph("<b>index.html — Functions 4-6 (continued)</b>", h3))
    S.append(cb(
        "// FUNCTION 4: placeOrder()\n"
        "// WHAT: Triggers checkout. Backend decrements stock, clears cart, saves order.\n"
        "// HTTP: POST /orders/{userId}\n"
        "async function placeOrder() {\n"
        "    let res = await fetch(`http://localhost:8080/orders/${userId}`, { method: 'POST' });\n"
        "    let data = await res.json();\n"
        "    if (!res.ok) return alert('Checkout Failed: ' + data.message);\n"
        "    alert(`Order #${data.data.id} placed! Total: Rs${data.data.totalPrice}`);\n"
        "    document.getElementById('cartPanel').classList.remove('active');\n"
        "    loadBooks(); loadCart(); loadOrders();  // Refresh everything\n"
        "}\n\n"
        "// FUNCTION 5: loadOrders()\n"
        "// WHAT: Fetches and displays order history for current user\n"
        "// HTTP: GET /orders/{userId}\n"
        "async function loadOrders() {\n"
        "    let res = await fetch(`http://localhost:8080/orders/${userId}`);\n"
        "    let data = await res.json();\n"
        "    data.data.forEach(o => { /* Render: Order #ID, userId, totalPrice */ });\n"
        "    document.getElementById('orders').innerHTML = html;\n"
        "}\n\n"
        "// FUNCTION 6: toggleCart()\n"
        "// WHAT: Slides cart panel in/out using CSS class toggle\n"
        "function toggleCart() {\n"
        "    let panel = document.getElementById('cartPanel');\n"
        "    panel.classList.toggle('active');       // CSS: right: -420px -> right: 0\n"
        "    if (panel.classList.contains('active')) loadCart();\n"
        "}\n\n"
        "// INITIALIZATION: runs when page loads\n"
        "loadBooks(); loadCart(); loadOrders();", cf))
    S.append(Spacer(1,6))

    S.append(Paragraph("<b>FILE 18: admin.html</b> (Admin Dashboard) — All JavaScript Functions", h2))
    S.append(cb(
        "// ═══════════════════════════════════════════════════════════════\n"
        "// IMAGE PREVIEW EVENT LISTENER\n"
        "// WHAT: Shows instant preview when admin selects an image file\n"
        "// ═══════════════════════════════════════════════════════════════\n"
        "document.getElementById('imageFile').onchange = function(e) {\n"
        "    let preview = document.getElementById('preview');\n"
        "    preview.src = URL.createObjectURL(e.target.files[0]);  // Client-side blob URL\n"
        "    preview.style.display = 'block';                       // Make visible\n"
        "};\n\n"
        "// ═══════════════════════════════════════════════════════════════\n"
        "// FUNCTION: addBook()\n"
        "// WHAT: Uploads image + saves book to catalog (2-step process)\n"
        "// HTTP STEP 1: POST /books/upload (multipart/form-data) -> returns image URL\n"
        "// HTTP STEP 2: POST /books (application/json) -> saves Book entity\n"
        "// ═══════════════════════════════════════════════════════════════\n"
        "async function addBook() {\n"
        "    // Read form inputs\n"
        "    let title = document.getElementById('title').value;\n"
        "    let author = document.getElementById('author').value;\n"
        "    let price = parseFloat(document.getElementById('price').value);\n"
        "    let quantity = parseInt(document.getElementById('quantity').value);\n"
        "    let imageUrl = document.getElementById('imageUrl').value;\n\n"
        "    // Validate required fields\n"
        "    if (!title || !author || isNaN(price) || isNaN(quantity)) return alert('Fill all fields');\n\n"
        "    // STEP 1: Upload image file (if selected)\n"
        "    if (fileInput.files.length > 0) {\n"
        "        let formData = new FormData();\n"
        "        formData.append('file', fileInput.files[0]);\n"
        "        let res = await fetch('http://localhost:8080/books/upload', { method: 'POST', body: formData });\n"
        "        imageUrl = await res.text();  // e.g. 'http://localhost:8080/uploads/1740000000_cover.jpg'\n"
        "    }\n\n"
        "    // STEP 2: Save book entity\n"
        "    let book = { title, author, price, quantity, imageUrl };\n"
        "    let response = await fetch('http://localhost:8080/books', {\n"
        "        method: 'POST',\n"
        "        headers: { 'Content-Type': 'application/json' },\n"
        "        body: JSON.stringify(book)\n"
        "    });\n"
        "    let json = await response.json();\n"
        "    if (response.ok && json.success) {\n"
        "        alert(`Book \"${json.data.title}\" added!`);\n"
        "        loadBooks();  // Refresh grid\n"
        "    }\n"
        "}\n\n"
        "// ═══════════════════════════════════════════════════════════════\n"
        "// FUNCTION: loadBooks() — same as index.html but with Delete buttons\n"
        "// HTTP: GET /books\n"
        "// ═══════════════════════════════════════════════════════════════\n"
        "async function loadBooks() { /* Renders cards with Delete button */ }\n\n"
        "// ═══════════════════════════════════════════════════════════════\n"
        "// FUNCTION: deleteBook(id)\n"
        "// WHAT: Confirms and deletes book from catalog\n"
        "// HTTP: DELETE /books/{id}\n"
        "// ═══════════════════════════════════════════════════════════════\n"
        "async function deleteBook(id) {\n"
        "    if (!confirm('Delete this book?')) return;\n"
        "    let res = await fetch('http://localhost:8080/books/' + id, { method: 'DELETE' });\n"
        "    if (res.ok) { alert('Deleted!'); loadBooks(); }\n"
        "}\n\n"
        "// INITIALIZATION\n"
        "loadBooks();", cf))
    S.append(PageBreak())

    # ═══════════════════════════════════════════════════════════════════════
    # SECTION 6: END-TO-END WORKFLOWS
    # ═══════════════════════════════════════════════════════════════════════
    S.append(Paragraph("Section 6 — End-to-End Workflow: What Happens When Each Action Is Selected", h1))

    workflows = [
        ("A. Page Load (Customer Opens index.html)", [
            "1. Browser loads http://localhost:8080/index.html from Spring's static/ folder",
            "2. HTML/CSS renders. <script> block executes immediately.",
            "3. Calls loadBooks() -> fetch GET /books -> BookController.getBooks() -> BookService.getAllBooks() -> BookRepository.findAll() -> SQL: SELECT * FROM book -> returns List<Book> -> ApiResponse JSON",
            "4. Calls loadCart() -> fetch GET /cart -> CartController.get() -> CartService.getCart() -> CartRepository.findAll() -> SQL: SELECT * FROM cart_item JOIN book -> returns List<CartItem> JSON",
            "5. Calls loadOrders() -> fetch GET /orders/user1 -> OrderController.getOrders('user1') -> OrderService.getOrdersByUser('user1') -> OrderRepository.findByUserId('user1') -> SQL: SELECT * FROM orders WHERE user_id = 'user1'",
            "6. JavaScript builds HTML cards from JSON data and injects into DOM",
        ]),
        ("B. Customer Clicks 'Add to Cart'", [
            "1. onclick='addToCart(1, 10)' triggers JavaScript function",
            "2. Reads qty from input #qty-1 (e.g., qty=2)",
            "3. Client validation: qty > 0? YES. qty <= stock(10)? YES.",
            "4. fetch('http://localhost:8080/cart/1/2', { method: 'POST' })",
            "5. Tomcat -> DispatcherServlet -> CartController.add(id=1, qty=2)",
            "6. CartService.addToCart(1, 2):",
            "   a) bookRepo.findById(1) -> SQL: SELECT * FROM book WHERE id = 1 -> Book found",
            "   b) qty(2) > book.quantity(10)? NO -> proceed",
            "   c) Create CartItem(book=Book#1, quantity=2)",
            "   d) cartRepo.save(item) -> SQL: INSERT INTO cart_item (book_id, quantity) VALUES (1, 2)",
            "7. Returns ApiResponse(true, 'Added', CartItem) -> JSON -> HTTP 200 OK",
            "8. Frontend: alert('Added!'), calls loadBooks() + loadCart() to refresh UI",
        ]),
        ("C. Customer Clicks 'Place Order'", [
            "1. onclick='placeOrder()' triggers JavaScript function",
            "2. fetch('http://localhost:8080/orders/user1', { method: 'POST' })",
            "3. Tomcat -> DispatcherServlet -> OrderController.placeOrder('user1')",
            "4. OrderService.placeOrder('user1'):",
            "   a) cartRepo.findAll() -> SQL: SELECT * FROM cart_item -> gets 1 item: CartItem(book=Book#1, qty=2)",
            "   b) items.isEmpty()? NO -> proceed",
            "   c) For CartItem(Book#1, qty=2):",
            "      - item.qty(2) > book.qty(10)? NO -> proceed",
            "      - total += 2 * 499.0 = 998.0",
            "      - book.setQuantity(10 - 2 = 8) -> bookRepo.save(book) -> SQL: UPDATE book SET quantity = 8 WHERE id = 1",
            "   d) cartRepo.deleteAll() -> SQL: DELETE FROM cart_item",
            "   e) Create Order(totalPrice=998.0, userId='user1')",
            "   f) orderRepo.save(order) -> SQL: INSERT INTO orders (total_price, user_id) VALUES (998.0, 'user1')",
            "5. Returns ApiResponse(true, 'Order placed', Order#1) -> JSON -> HTTP 200",
            "6. Frontend: alert('Order #1 placed! Total: Rs998'), closes cart drawer",
            "7. Calls loadBooks() (stock now shows 8), loadCart() (badge shows 0), loadOrders() (shows Order #1)",
        ]),
        ("D. Admin Adds a Book (admin.html)", [
            "1. Admin fills: title='Clean Code', author='Robert Martin', price=499, quantity=10",
            "2. Admin selects cover image file -> onchange preview renders instantly via URL.createObjectURL()",
            "3. Admin clicks 'Add Book' -> addBook() executes",
            "4. STEP 1 — Image Upload:",
            "   a) new FormData().append('file', imageFile)",
            "   b) fetch POST /books/upload with body: formData (multipart/form-data)",
            "   c) BookController.uploadImage(): creates uploads/ dir, saves file as 1740000000_cover.jpg",
            "   d) Returns text: 'http://localhost:8080/uploads/1740000000_cover.jpg'",
            "5. STEP 2 — Save Book:",
            "   a) Builds JSON: {title, author, price, quantity, imageUrl}",
            "   b) fetch POST /books with Content-Type: application/json",
            "   c) BookController.addBook() -> @RequestBody deserializes JSON into Book object",
            "   d) BookService.saveBook(book) -> BookRepository.save(book) -> SQL: INSERT INTO book (title, author, price, quantity, image_url) VALUES (...)",
            "6. Returns ApiResponse(true, 'Book added', Book#1) -> JSON -> HTTP 200",
            "7. Frontend: alert('Book added!'), clears form, calls loadBooks() to refresh grid",
        ]),
        ("E. Admin Deletes a Book", [
            "1. Admin clicks 'Delete' on book card -> deleteBook(1) executes",
            "2. confirm('Delete this book?') -> User clicks OK",
            "3. fetch('http://localhost:8080/books/1', { method: 'DELETE' })",
            "4. BookController.deleteBook(1) -> BookService.deleteBook(1) -> BookRepository.deleteById(1)",
            "5. SQL: DELETE FROM book WHERE id = 1",
            "6. Returns ApiResponse(true, 'Book deleted', null) -> HTTP 200",
            "7. Frontend: alert('Deleted!'), calls loadBooks() to remove card from grid",
        ]),
    ]
    for title, steps in workflows:
        S.append(Paragraph(f"<b>{title}</b>", h2))
        S.append(flow_box(steps, cf, bg="#f0f9ff", border="#0284c7"))
        S.append(Spacer(1,4))

    S.append(PageBreak())

    # ═══════════════════════════════════════════════════════════════════════
    # SECTION 7: REST API TABLE
    # ═══════════════════════════════════════════════════════════════════════
    S.append(Paragraph("Section 7 — Master REST API Reference Table &amp; SQL Query Map", h1))

    api_rows = [
        [Paragraph("<b>Endpoint</b>",h3), Paragraph("<b>Controller.Method()</b>",h3), Paragraph("<b>Service.Method()</b>",h3), Paragraph("<b>SQL Executed</b>",h3), Paragraph("<b>Called From</b>",h3)],
        [Paragraph("GET /books",bl), Paragraph("BookController.getBooks()",bl), Paragraph("BookService.getAllBooks()",bl), Paragraph("SELECT * FROM book",bl), Paragraph("index + admin",bl)],
        [Paragraph("POST /books",bl), Paragraph("BookController.addBook()",bl), Paragraph("BookService.saveBook()",bl), Paragraph("INSERT INTO book ...",bl), Paragraph("admin",bl)],
        [Paragraph("DELETE /books/{id}",bl), Paragraph("BookController.deleteBook()",bl), Paragraph("BookService.deleteBook()",bl), Paragraph("DELETE FROM book WHERE id=?",bl), Paragraph("admin",bl)],
        [Paragraph("POST /books/upload",bl), Paragraph("BookController.uploadImage()",bl), Paragraph("(filesystem I/O)",bl), Paragraph("(no SQL)",bl), Paragraph("admin",bl)],
        [Paragraph("POST /cart/{id}/{qty}",bl), Paragraph("CartController.add()",bl), Paragraph("CartService.addToCart()",bl), Paragraph("SELECT book; INSERT cart_item",bl), Paragraph("index",bl)],
        [Paragraph("GET /cart",bl), Paragraph("CartController.get()",bl), Paragraph("CartService.getCart()",bl), Paragraph("SELECT * FROM cart_item JOIN book",bl), Paragraph("index",bl)],
        [Paragraph("POST /orders/{userId}",bl), Paragraph("OrderController.placeOrder()",bl), Paragraph("OrderService.placeOrder()",bl), Paragraph("SELECT cart; UPDATE book; DELETE cart; INSERT orders",bl), Paragraph("index",bl)],
        [Paragraph("GET /orders/{userId}",bl), Paragraph("OrderController.getOrders()",bl), Paragraph("OrderService.getOrdersByUser()",bl), Paragraph("SELECT * FROM orders WHERE user_id=?",bl), Paragraph("index",bl)],
    ]
    at = Table(api_rows, colWidths=[85, 105, 100, 105, 55])
    at.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,0),colors.HexColor("#1d3557")),
        ('TEXTCOLOR',(0,0),(-1,0),colors.white),
        ('BOX',(0,0),(-1,-1),1,colors.HexColor("#cbd5e1")),
        ('INNERGRID',(0,0),(-1,-1),0.5,colors.HexColor("#e2e8f0")),
        ('LEFTPADDING',(0,0),(-1,-1),4),('RIGHTPADDING',(0,0),(-1,-1),4),
        ('TOPPADDING',(0,0),(-1,-1),3),('BOTTOMPADDING',(0,0),(-1,-1),3),
        ('VALIGN',(0,0),(-1,-1),'TOP'),
    ]))
    S.append(at)
    S.append(PageBreak())

    # ═══════════════════════════════════════════════════════════════════════
    # SECTION 8: CRUD
    # ═══════════════════════════════════════════════════════════════════════
    S.append(Paragraph("Section 8 — CRUD Operations Explained With Code", h1))
    S.append(Paragraph("CRUD = Create, Read, Update, Delete. Here is how each operation works in BookHub:", b))
    S.append(Spacer(1,3))

    crud_rows = [
        [Paragraph("<b>Operation</b>",h3), Paragraph("<b>HTTP Method</b>",h3), Paragraph("<b>Example Endpoint</b>",h3), Paragraph("<b>Java Code</b>",h3), Paragraph("<b>SQL</b>",h3)],
        [Paragraph("CREATE",bl), Paragraph("POST",bl), Paragraph("POST /books",bl), Paragraph("repo.save(book)",bl), Paragraph("INSERT INTO book ...",bl)],
        [Paragraph("READ (all)",bl), Paragraph("GET",bl), Paragraph("GET /books",bl), Paragraph("repo.findAll()",bl), Paragraph("SELECT * FROM book",bl)],
        [Paragraph("READ (one)",bl), Paragraph("GET",bl), Paragraph("GET /books/{id}",bl), Paragraph("repo.findById(id)",bl), Paragraph("SELECT * FROM book WHERE id=?",bl)],
        [Paragraph("UPDATE",bl), Paragraph("PUT/POST",bl), Paragraph("POST /books",bl), Paragraph("repo.save(book) [if id exists]",bl), Paragraph("UPDATE book SET ... WHERE id=?",bl)],
        [Paragraph("DELETE",bl), Paragraph("DELETE",bl), Paragraph("DELETE /books/{id}",bl), Paragraph("repo.deleteById(id)",bl), Paragraph("DELETE FROM book WHERE id=?",bl)],
    ]
    ct = Table(crud_rows, colWidths=[60, 60, 95, 125, 110])
    ct.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,0),colors.HexColor("#2a9d8f")),
        ('TEXTCOLOR',(0,0),(-1,0),colors.white),
        ('BOX',(0,0),(-1,-1),1,colors.HexColor("#cbd5e1")),
        ('INNERGRID',(0,0),(-1,-1),0.5,colors.HexColor("#e2e8f0")),
        ('LEFTPADDING',(0,0),(-1,-1),4),('RIGHTPADDING',(0,0),(-1,-1),4),
        ('TOPPADDING',(0,0),(-1,-1),3),('BOTTOMPADDING',(0,0),(-1,-1),3),
        ('VALIGN',(0,0),(-1,-1),'TOP'),
    ]))
    S.append(ct)
    S.append(Spacer(1,10))

    # ═══════════════════════════════════════════════════════════════════════
    # SECTION 9: EXCEPTION HANDLING
    # ═══════════════════════════════════════════════════════════════════════
    S.append(Paragraph("Section 9 — Exception Handling Pipeline", h1))
    S.append(Paragraph("What happens when something goes wrong — traced from service to browser:", b))
    exception_flow = [
        "Example: Customer tries to add 100 copies of a book that only has 10 in stock",
        "",
        "1. Frontend: fetch('http://localhost:8080/cart/1/100', { method: 'POST' })",
        "2. CartController.add(id=1, qty=100) -> CartService.addToCart(1, 100)",
        "3. CartService: bookRepo.findById(1) -> Book found (stock = 10)",
        "4. CartService: 100 > 10? YES -> throw new RuntimeException('Stock not available')",
        "5. Exception bubbles up from Service -> Controller -> DispatcherServlet",
        "6. GlobalExceptionHandler intercepts (because of @ControllerAdvice + @ExceptionHandler)",
        "7. handleRuntimeException(ex) creates: ApiResponse(false, 'Stock not available', null)",
        "8. Returns: ResponseEntity with HTTP 400 BAD REQUEST status",
        "9. Tomcat sends response: { \"success\": false, \"message\": \"Stock not available\", \"data\": null }",
        "10. Frontend: res.ok is false -> alert('Error: Stock not available')",
    ]
    S.append(flow_box(exception_flow, cf, bg="#fef2f2", border="#dc2626"))
    S.append(Spacer(1,8))

    eh_table = [
        [Paragraph("<b>Exception Type</b>",h3), Paragraph("<b>Thrown By</b>",h3), Paragraph("<b>Message</b>",h3), Paragraph("<b>HTTP Status</b>",h3)],
        [Paragraph("RuntimeException",bl), Paragraph("CartService.addToCart()",bl), Paragraph("'Book not found'",bl), Paragraph("400 Bad Request",bl)],
        [Paragraph("RuntimeException",bl), Paragraph("CartService.addToCart()",bl), Paragraph("'Stock not available'",bl), Paragraph("400 Bad Request",bl)],
        [Paragraph("RuntimeException",bl), Paragraph("OrderService.placeOrder()",bl), Paragraph("'Cart is empty'",bl), Paragraph("400 Bad Request",bl)],
        [Paragraph("RuntimeException",bl), Paragraph("OrderService.placeOrder()",bl), Paragraph("'Stock not available'",bl), Paragraph("400 Bad Request",bl)],
        [Paragraph("Exception (any other)",bl), Paragraph("Any layer",bl), Paragraph("'Something went wrong'",bl), Paragraph("500 Internal Error",bl)],
    ]
    et = Table(eh_table, colWidths=[95, 110, 110, 95])
    et.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,0),colors.HexColor("#dc2626")),
        ('TEXTCOLOR',(0,0),(-1,0),colors.white),
        ('BOX',(0,0),(-1,-1),1,colors.HexColor("#cbd5e1")),
        ('INNERGRID',(0,0),(-1,-1),0.5,colors.HexColor("#e2e8f0")),
        ('LEFTPADDING',(0,0),(-1,-1),4),('RIGHTPADDING',(0,0),(-1,-1),4),
        ('TOPPADDING',(0,0),(-1,-1),3),('BOTTOMPADDING',(0,0),(-1,-1),3),
        ('VALIGN',(0,0),(-1,-1),'TOP'),
    ]))
    S.append(et)
    S.append(PageBreak())

    # ═══════════════════════════════════════════════════════════════════════
    # SECTION 10: INTERVIEW CLOSING
    # ═══════════════════════════════════════════════════════════════════════
    S.append(Paragraph("Section 10 — Interview Closing Summary &amp; Golden Pitch", h1))
    S.append(Spacer(1,4))

    S.append(callout(
        "<b>30-Second Pitch (memorize this):</b><br/>"
        "\"BookHub is a full-stack e-commerce bookstore application built with <b>Java 21</b> and <b>Spring Boot 4.0.5</b> on the backend, <b>MySQL</b> as the relational database, and <b>HTML5/CSS3/JavaScript</b> on the frontend.<br/><br/>"
        "I structured the backend using a clean <b>3-tier layered architecture</b>: <b>Controllers</b> (REST endpoints) &rarr; <b>Services</b> (business logic) &rarr; <b>Repositories</b> (database access via Spring Data JPA/Hibernate).<br/><br/>"
        "The frontend connects to the backend using the <b>JavaScript Fetch API</b> to call RESTful endpoints. All responses are standardized using a generic <b>ApiResponse&lt;T&gt;</b> DTO. <b>@CrossOrigin</b> enables CORS, and a <b>GlobalExceptionHandler</b> with @ControllerAdvice converts all errors into clean JSON responses with proper HTTP status codes.<br/><br/>"
        "Key features include: <b>catalog CRUD management</b> with cover image upload, <b>shopping cart</b> with real-time stock validation, <b>checkout workflow</b> with automatic inventory deduction, and <b>order history</b> per user.\"",
        cb_style, title="INTERVIEW GOLDEN PITCH — MEMORIZE THIS", bg="#f0fdf4", border="#16a34a"
    ))
    S.append(Spacer(1,8))

    S.append(callout(
        "<b>Architecture Diagram:</b><br/>"
        "<font face='Courier' size='7.5'>"
        "[Browser: index.html / admin.html]<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|  JavaScript Fetch API (HTTP GET/POST/DELETE + JSON)<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;v<br/>"
        "[Embedded Tomcat :8080] &rarr; [DispatcherServlet] &rarr; [@CrossOrigin CORS]<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;v<br/>"
        "[@RestController] &rarr; parses @PathVariable, @RequestBody, @RequestParam<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;v<br/>"
        "[@Service] &rarr; Business rules, validation, stock checks, price calculations<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;v<br/>"
        "[JpaRepository] &rarr; Spring Data JPA dynamic proxy &rarr; Hibernate ORM<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;v<br/>"
        "[HikariCP Connection Pool] &rarr; [mysql-connector-j JDBC Driver]<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;v<br/>"
        "[MySQL Server :3306] &rarr; bookstore_db &rarr; Tables: book, cart_item, orders<br/>"
        "</font>",
        cb_style, title="FULL SYSTEM ARCHITECTURE", bg="#f8fafc", border="#1d3557"
    ))
    S.append(Spacer(1,8))

    S.append(callout(
        "<b>Layer Responsibility Summary:</b><br/>"
        "&bull; <b>Controller Layer:</b> Receives HTTP requests, extracts parameters, delegates to Service, wraps response in ApiResponse, returns JSON.<br/>"
        "&bull; <b>Service Layer:</b> Contains ALL business logic — validation, stock checks, price calculations, cart operations. NEVER touches HTTP directly.<br/>"
        "&bull; <b>Repository Layer:</b> Pure data access. Extends JpaRepository. Zero business logic. Spring generates SQL implementation automatically.<br/>"
        "&bull; <b>Entity Layer:</b> Defines database table schema in Java. @Entity + @Id + @GeneratedValue = table with auto-increment PK.<br/>"
        "&bull; <b>DTO Layer:</b> ApiResponse&lt;T&gt; standardizes every API response format for frontend consumption.<br/>"
        "&bull; <b>Exception Layer:</b> @ControllerAdvice catches ALL errors globally, returns proper HTTP 400/500 status codes with JSON error messages.<br/>"
        "&bull; <b>Frontend Layer:</b> HTML/CSS/JS pages call backend REST APIs via fetch(), parse JSON responses, and dynamically update the DOM.",
        cb_style, title="WHAT EACH LAYER DOES — QUICK REFERENCE", bg="#fef3c7", border="#d97706"
    ))

    # build
    doc.build(S, canvasmaker=NumberedCanvas)
    print(f"[SUCCESS] PDF generated: {fname}")

if __name__ == "__main__":
    generate_pdf()
