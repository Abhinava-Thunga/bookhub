import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas

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
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#555555"))
        
        # Don't draw running header/footer on cover page if page 1
        if self._pageNumber > 1:
            # Running header
            self.drawString(54, letter[1] - 36, "BookHub — Full-Stack Technical Documentation & Interview Guide")
            self.setStrokeColor(colors.HexColor("#dddddd"))
            self.setLineWidth(0.5)
            self.line(54, letter[1] - 42, letter[0] - 54, letter[1] - 42)
            
            # Running footer
            page_text = f"Page {self._pageNumber} of {page_count}"
            self.drawRightString(letter[0] - 54, 36, page_text)
            self.drawString(54, 36, "Confidential & Proprietary — Prepared for Technical Review & Interview Prep")
            self.line(54, 48, letter[0] - 54, 48)
        self.restoreState()

def build_pdf(filename="BookHub_Complete_Documentation_and_Interview_Guide.pdf"):
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=28,
        textColor=colors.HexColor("#1d3557"),
        spaceAfter=8
    )

    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor("#457b9d"),
        spaceAfter=15
    )

    h1_style = ParagraphStyle(
        'SectionH1',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=15,
        leading=19,
        textColor=colors.HexColor("#1d3557"),
        spaceBefore=14,
        spaceAfter=8,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'SectionH2',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor("#2a9d8f"),
        spaceBefore=10,
        spaceAfter=5,
        keepWithNext=True
    )

    h3_style = ParagraphStyle(
        'SectionH3',
        parent=styles['Heading3'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=13,
        textColor=colors.HexColor("#e76f51"),
        spaceBefore=8,
        spaceAfter=4,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'BodyDark',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        textColor=colors.HexColor("#222222"),
        spaceAfter=6
    )

    bullet_style = ParagraphStyle(
        'BulletText',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=colors.HexColor("#222222"),
        leftIndent=15,
        spaceAfter=4
    )

    code_style = ParagraphStyle(
        'CodeSnippet',
        parent=styles['Code'],
        fontName='Courier',
        fontSize=8,
        leading=10.5,
        textColor=colors.HexColor("#111111")
    )

    callout_style = ParagraphStyle(
        'CalloutText',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=9,
        leading=13,
        textColor=colors.HexColor("#1d3557")
    )

    table_header_style = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11,
        textColor=colors.white
    )

    table_cell_style = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=10.5,
        textColor=colors.HexColor("#222222")
    )

    qa_q_style = ParagraphStyle(
        'QAQuestion',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=13.5,
        textColor=colors.HexColor("#1d3557"),
        spaceBefore=8,
        spaceAfter=3,
        keepWithNext=True
    )

    qa_a_style = ParagraphStyle(
        'QAAnswer',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=12.5,
        textColor=colors.HexColor("#333333"),
        leftIndent=10,
        spaceAfter=6
    )

    story = []

    def make_callout(text):
        p = Paragraph(text, callout_style)
        t = Table([[p]], colWidths=[letter[0] - 108])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#eef4f8")),
            ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#457b9d")),
            ('LINELEFT', (0,0), (-1,-1), 4, colors.HexColor("#1d3557")),
            ('TOPPADDING', (0,0), (-1,-1), 6),
            ('BOTTOMPADDING', (0,0), (-1,-1), 6),
            ('LEFTPADDING', (0,0), (-1,-1), 10),
            ('RIGHTPADDING', (0,0), (-1,-1), 10),
        ]))
        return t

    def make_code_box(code_text):
        # Escape xml chars
        esc = code_text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('\n', '<br/>').replace(' ', '&nbsp;')
        p = Paragraph(esc, code_style)
        t = Table([[p]], colWidths=[letter[0] - 108])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#f8f9fa")),
            ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor("#ced4da")),
            ('TOPPADDING', (0,0), (-1,-1), 5),
            ('BOTTOMPADDING', (0,0), (-1,-1), 5),
            ('LEFTPADDING', (0,0), (-1,-1), 8),
            ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ]))
        return t

    # =========================================================================
    # COVER / TITLE
    # =========================================================================
    story.append(Spacer(1, 15))
    story.append(Paragraph("📚 BookHub Full-Stack Project", title_style))
    story.append(Paragraph("Complete Technical Documentation, Code Architecture & Interview Preparation Manual", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor("#1d3557"), spaceAfter=12))

    meta_text = (
        "<b>Core Technologies:</b> Java 21 LTS | Spring Boot 4.0.5 | Spring Web MVC | Spring Data JPA | "
        "Hibernate | MySQL 8.0+ | HTML5 / CSS3 / Vanilla JS<br/>"
        "<b>Architectural Style:</b> Decoupled Layered MVC &amp; Stateless RESTful APIs | <b>Author / Maintainer:</b> Abhinava Thunga"
    )
    story.append(make_callout(meta_text))
    story.append(Spacer(1, 10))

    # =========================================================================
    # 1. PROJECT OVERVIEW
    # =========================================================================
    story.append(Paragraph("1. Project Overview", h1_style))
    story.append(Paragraph(
        "<b>BookHub</b> is an enterprise-grade full-stack web application designed for online book retail and inventory management. "
        "It couples an interactive client storefront and administration management portal with an enterprise Spring Boot REST API "
        "backed by MySQL relational persistence.", body_style
    ))
    story.append(Paragraph("<b>Key Problems Solved:</b>", h2_style))
    story.append(Paragraph("• <b>Accurate Inventory Control:</b> Prevents overselling by checking stock on both frontend and backend before cart creation and deducting inventory atomically upon checkout.", bullet_style))
    story.append(Paragraph("• <b>Decoupled Architecture:</b> Clean separation between the presentation tier (vanilla JS Fetch API), business services, and database persistence layers.", bullet_style))
    story.append(Paragraph("• <b>Digital Media Management:</b> Dedicated endpoint handling multipart image uploads and exposing local storage over HTTP via custom Spring MVC resource handlers.", bullet_style))
    story.append(Paragraph("• <b>Auditability &amp; History:</b> Every placed order is permanently stored with calculated totals and user identifiers, providing full historical visibility.", bullet_style))

    # =========================================================================
    # 2. COMPLETE TECH STACK
    # =========================================================================
    story.append(Spacer(1, 8))
    story.append(Paragraph("2. Complete Tech Stack & Technology Evaluation", h1_style))
    
    stack_data = [
        [Paragraph("Technology", table_header_style), Paragraph("Version", table_header_style), Paragraph("Role in BookHub", table_header_style), Paragraph("Why Selected vs. Alternatives", table_header_style)],
        [Paragraph("<b>Java</b>", table_cell_style), Paragraph("21 (LTS)", table_cell_style), Paragraph("Core backend programming language", table_cell_style), Paragraph("Enterprise-grade type safety, long-term support, and modern performance.", table_cell_style)],
        [Paragraph("<b>Spring Boot</b>", table_cell_style), Paragraph("4.0.5", table_cell_style), Paragraph("Application framework & IoC container", table_cell_style), Paragraph("Opinionated auto-configuration, embedded Tomcat server, rapid setup.", table_cell_style)],
        [Paragraph("<b>Spring Web MVC</b>", table_cell_style), Paragraph("4.0.5", table_cell_style), Paragraph("RESTful HTTP controller layer", table_cell_style), Paragraph("DispatcherServlet routing, parameter parsing, and CORS support.", table_cell_style)],
        [Paragraph("<b>Spring Data JPA</b>", table_cell_style), Paragraph("4.0.5", table_cell_style), Paragraph("Data access abstraction", table_cell_style), Paragraph("Eliminates boilerplate JDBC; provides dynamic query synthesis.", table_cell_style)],
        [Paragraph("<b>Hibernate</b>", table_cell_style), Paragraph("7.x (Jakarta)", table_cell_style), Paragraph("Object-Relational Mapping (ORM)", table_cell_style), Paragraph("Translates Java entities to MySQL DDL/DML, manages foreign keys.", table_cell_style)],
        [Paragraph("<b>MySQL</b>", table_cell_style), Paragraph("8.0+", table_cell_style), Paragraph("Relational Database Management System", table_cell_style), Paragraph("ACID transactional consistency, foreign key constraints, high throughput.", table_cell_style)],
        [Paragraph("<b>Vanilla HTML5/CSS3/JS</b>", table_cell_style), Paragraph("ES6+", table_cell_style), Paragraph("Customer storefront & Admin portal", table_cell_style), Paragraph("Zero framework bloat, fast load times, native Fetch API communication.", table_cell_style)],
        [Paragraph("<b>Maven</b>", table_cell_style), Paragraph("3.9+", table_cell_style), Paragraph("Build & dependency automation", table_cell_style), Paragraph("Manages dependencies and builds reproducible standalone executables.", table_cell_style)]
    ]
    t_stack = Table(stack_data, colWidths=[90, 50, 150, 214])
    t_stack.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#1d3557")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cccccc")),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#f8f9fa")]),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_stack)

    # =========================================================================
    # 3. COMPLETE PROJECT STRUCTURE
    # =========================================================================
    story.append(Spacer(1, 10))
    story.append(Paragraph("3. Complete Project Structure", h1_style))
    struct_code = (
        "bookstore/\n"
        "├── uploads/                            # Disk storage for uploaded cover images\n"
        "├── src/main/java/com/bookhub/bookstore/\n"
        "│   ├── BookstoreApplication.java       # Startup class & /uploads/** web resource handler\n"
        "│   ├── controller/                     # REST HTTP presentation layer\n"
        "│   │   ├── BookController.java         # /books endpoints (CRUD & image upload)\n"
        "│   │   ├── CartController.java         # /cart endpoints (add item, view cart)\n"
        "│   │   └── OrderController.java        # /orders endpoints (checkout, history)\n"
        "│   ├── service/                        # Business logic layer\n"
        "│   │   ├── BookService.java            # Catalog business logic & repository mediation\n"
        "│   │   ├── CartService.java            # Stock validation & cart item persistence\n"
        "│   │   └── OrderService.java           # Checkout orchestration & inventory decrement\n"
        "│   ├── repository/                     # Data access layer (Spring Data JPA interfaces)\n"
        "│   │   ├── BookRepository.java         # JpaRepository<Book, Long>\n"
        "│   │   ├── CartRepository.java         # JpaRepository<CartItem, Long>\n"
        "│   │   └── OrderRepository.java        # JpaRepository<Order, Long> with findByUserId\n"
        "│   ├── entity/                         # Database entities (Hibernate mappings)\n"
        "│   │   ├── Book.java                   # book table mapping\n"
        "│   │   ├── CartItem.java               # cart_item table mapping (@ManyToOne Book)\n"
        "│   │   └── Order.java                  # orders table mapping (escapes MySQL keyword)\n"
        "│   ├── dto/                            # Data Transfer Objects\n"
        "│   │   └── ApiResponse.java            # Generic envelope { success, message, data }\n"
        "│   └── exception/                      # Centralized error handling\n"
        "│       └── GlobalExceptionHandler.java # @ControllerAdvice converting errors to HTTP 400/500\n"
        "├── src/main/resources/\n"
        "│   ├── application.properties          # MySQL credentials, Hibernate DDL, server port\n"
        "│   └── static/                         # Frontend web interfaces\n"
        "│       ├── index.html                  # Customer storefront (browsing, cart drawer)\n"
        "│       └── admin.html                  # Admin portal (add books, upload covers)\n"
        "└── pom.xml                             # Maven configuration & dependencies"
    )
    story.append(make_code_box(struct_code))

    # =========================================================================
    # 4. APPLICATION ENTRY POINT & STARTUP
    # =========================================================================
    story.append(PageBreak())
    story.append(Paragraph("4. Application Entry Point & Startup Flow", h1_style))
    story.append(Paragraph(
        "<b>File:</b> <code>BookstoreApplication.java</code> &nbsp;|&nbsp; <b>Method:</b> <code>public static void main(String[] args)</code>", body_style
    ))
    story.append(Paragraph(
        "When the application is launched (e.g. via <code>./mvnw spring-boot:run</code>), the JVM executes <code>main()</code>. "
        "The complete startup lifecycle proceeds through 6 distinct stages:", body_style
    ))
    story.append(Paragraph("<b>Step 1 — Bootstrap:</b> <code>SpringApplication.run()</code> initializes the <code>ApplicationContext</code> and loads configuration properties from <code>src/main/resources/application.properties</code>.", bullet_style))
    story.append(Paragraph("<b>Step 2 — Dependency &amp; Autoconfiguration Scan:</b> Spring detects Spring MVC, Spring Data JPA, Hibernate, and MySQL Connector on the classpath.", bullet_style))
    story.append(Paragraph("<b>Step 3 — Component Scanning:</b> Spring scans package <code>com.bookhub.bookstore</code> and subpackages. It discovers and registers `@RestController`, `@Service`, `@Repository`, and `@ControllerAdvice` beans into the IoC container.", bullet_style))
    story.append(Paragraph("<b>Step 4 — Resource Handler Registration:</b> The <code>config()</code> method registers a custom <code>WebMvcConfigurer</code> mapping HTTP requests for <code>/uploads/**</code> directly to the local directory <code>file:uploads/</code>.", bullet_style))
    story.append(Paragraph("<b>Step 5 — Database Connection &amp; Schema DDL:</b> HikariCP establishes a connection pool to MySQL (<code>bookstore_db</code>). Hibernate applies <code>ddl-auto=update</code>, synchronizing entity mappings with relational tables.", bullet_style))
    story.append(Paragraph("<b>Step 6 — Embedded Server Startup:</b> Apache Tomcat starts on TCP port <code>8080</code>. The Spring <code>DispatcherServlet</code> binds to root context (<code>/</code>), ready to process incoming requests.", bullet_style))

    # =========================================================================
    # 5. COMPLETE ARCHITECTURE & REQUEST FLOW
    # =========================================================================
    story.append(Spacer(1, 10))
    story.append(Paragraph("5. Complete Architecture & Request Flow", h1_style))
    story.append(Paragraph(
        "BookHub enforces a decoupled layered architecture. Communication flows unidirectionally from presentation to database:", body_style
    ))
    
    arch_flow = (
        "Frontend (Browser Fetch API)\n"
        "      │ HTTP Request (JSON / Multipart)\n"
        "      ▼\n"
        "Spring Web MVC Controller (BookController / CartController / OrderController)\n"
        "      │ Method Call & Parameter Passing (DTOs / Path Variables)\n"
        "      ▼\n"
        "Service Layer (BookService / CartService / OrderService)\n"
        "      │ Business Validation, Stock Calculations, Transaction Logic\n"
        "      ▼\n"
        "Repository Layer (BookRepository / CartRepository / OrderRepository)\n"
        "      │ Spring Data JPA Dynamic Proxies & JPQL Synthesis\n"
        "      ▼\n"
        "ORM & Driver Layer (Hibernate ORM 7.x & MySQL Connector/J)\n"
        "      │ JDBC PreparedStatement Execution over TCP Sockets\n"
        "      ▼\n"
        "MySQL Relational Database (bookstore_db: book, cart_item, orders tables)"
    )
    story.append(make_code_box(arch_flow))
    story.append(Spacer(1, 6))
    story.append(Paragraph("<b>Why Layers Are Separated:</b>", h2_style))
    story.append(Paragraph("• <b>Testability:</b> Service logic can be tested in isolation using Mockito mocks without needing a running database.", bullet_style))
    story.append(Paragraph("• <b>Maintainability:</b> Modifying database column types or table schemas only affects the Entity/Repository layers, leaving Controllers and Frontend intact.", bullet_style))
    story.append(Paragraph("• <b>Single Responsibility:</b> Controllers handle HTTP status and routing; Services execute business logic; Repositories manage database persistence.", bullet_style))

    # =========================================================================
    # 6. DATABASE DESIGN & STOCK OPERATIONS
    # =========================================================================
    story.append(Spacer(1, 10))
    story.append(Paragraph("6. Database Design & Inventory Operations", h1_style))
    story.append(Paragraph("BookHub utilizes three relational tables in the <code>bookstore_db</code> schema:", body_style))

    db_data = [
        [Paragraph("Table Name", table_header_style), Paragraph("Mapped Entity", table_header_style), Paragraph("Key Columns &amp; Constraints", table_header_style), Paragraph("Description", table_header_style)],
        [Paragraph("<code>book</code>", table_cell_style), Paragraph("<code>Book.java</code>", table_cell_style), Paragraph("<code>id</code> (PK, AUTO_INCREMENT)<br/><code>title</code>, <code>author</code>, <code>price</code><br/><code>quantity</code> (INT), <code>image_url</code>", table_cell_style), Paragraph("Stores the core book catalog and real-time inventory stock.", table_cell_style)],
        [Paragraph("<code>cart_item</code>", table_cell_style), Paragraph("<code>CartItem.java</code>", table_cell_style), Paragraph("<code>id</code> (PK, AUTO_INCREMENT)<br/><code>quantity</code> (INT)<br/><code>book_id</code> (FK -> book.id, @ManyToOne)", table_cell_style), Paragraph("Maintains active shopping cart items before checkout.", table_cell_style)],
        [Paragraph("<code>orders</code>", table_cell_style), Paragraph("<code>Order.java</code>", table_cell_style), Paragraph("<code>id</code> (PK, AUTO_INCREMENT)<br/><code>total_price</code> (DOUBLE)<br/><code>user_id</code> (VARCHAR, NOT NULL)", table_cell_style), Paragraph("Stores finalized customer purchases. Table name avoids MySQL reserved word.", table_cell_style)]
    ]
    t_db = Table(db_data, colWidths=[70, 85, 175, 174])
    t_db.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#1d3557")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cccccc")),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#f8f9fa")]),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_db)

    story.append(Spacer(1, 6))
    story.append(Paragraph("<b>Stock &amp; Checkout Mechanics:</b>", h2_style))
    story.append(Paragraph(
        "During <code>OrderService.placeOrder(userId)</code>, each cart item's requested quantity is compared against the warehouse stock. "
        "If available, the stock is decremented in-place: <code>book.setQuantity(book.getQuantity() - item.getQuantity())</code> and persisted via <code>bookRepo.save(book)</code>. "
        "The cart is cleared via <code>cartRepo.deleteAll()</code>, and an <code>Order</code> record is stored. "
        "If stock drops to zero, the book remains in the catalog with <code>quantity = 0</code>, preventing further additions until restocked.", body_style
    ))

    # =========================================================================
    # 7. COMPLETE REST API DOCUMENTATION
    # =========================================================================
    story.append(PageBreak())
    story.append(Paragraph("7. Complete REST API Documentation", h1_style))
    story.append(Paragraph(
        "All JSON responses are standardized using the generic envelope: <code>{ \"success\": boolean, \"message\": string, \"data\": object }</code>.", body_style
    ))

    api_data = [
        [Paragraph("Method &amp; Path", table_header_style), Paragraph("Controller Method", table_header_style), Paragraph("Parameters / Body", table_header_style), Paragraph("Success Response", table_header_style), Paragraph("Status", table_header_style)],
        [Paragraph("<b>GET</b> /books", table_cell_style), Paragraph("BookController.getBooks", table_cell_style), Paragraph("None", table_cell_style), Paragraph("ApiResponse&lt;List&lt;Book&gt;&gt;", table_cell_style), Paragraph("200 OK", table_cell_style)],
        [Paragraph("<b>POST</b> /books", table_cell_style), Paragraph("BookController.addBook", table_cell_style), Paragraph("Body: JSON Book object", table_cell_style), Paragraph("ApiResponse&lt;Book&gt;", table_cell_style), Paragraph("200 OK", table_cell_style)],
        [Paragraph("<b>DELETE</b> /books/{id}", table_cell_style), Paragraph("BookController.deleteBook", table_cell_style), Paragraph("Path: Long id", table_cell_style), Paragraph("ApiResponse&lt;String&gt;", table_cell_style), Paragraph("200 OK", table_cell_style)],
        [Paragraph("<b>POST</b> /books/upload", table_cell_style), Paragraph("BookController.uploadImage", table_cell_style), Paragraph("Multipart: file (image/*)", table_cell_style), Paragraph("String URL (served file path)", table_cell_style), Paragraph("200 OK", table_cell_style)],
        [Paragraph("<b>POST</b> /cart/{id}/{qty}", table_cell_style), Paragraph("CartController.add", table_cell_style), Paragraph("Path: Long id, int qty", table_cell_style), Paragraph("ApiResponse&lt;CartItem&gt;", table_cell_style), Paragraph("200/400", table_cell_style)],
        [Paragraph("<b>GET</b> /cart", table_cell_style), Paragraph("CartController.get", table_cell_style), Paragraph("None", table_cell_style), Paragraph("List&lt;CartItem&gt;", table_cell_style), Paragraph("200 OK", table_cell_style)],
        [Paragraph("<b>POST</b> /orders/{userId}", table_cell_style), Paragraph("OrderController.placeOrder", table_cell_style), Paragraph("Path: String userId", table_cell_style), Paragraph("ApiResponse&lt;Order&gt;", table_cell_style), Paragraph("200/400", table_cell_style)],
        [Paragraph("<b>GET</b> /orders/{userId}", table_cell_style), Paragraph("OrderController.getOrders", table_cell_style), Paragraph("Path: String userId", table_cell_style), Paragraph("ApiResponse&lt;List&lt;Order&gt;&gt;", table_cell_style), Paragraph("200 OK", table_cell_style)]
    ]
    t_api = Table(api_data, colWidths=[110, 115, 115, 115, 49])
    t_api.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#1d3557")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cccccc")),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#f8f9fa")]),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_api)

    # =========================================================================
    # 8. HOW TO RUN THE PROJECT
    # =========================================================================
    story.append(Spacer(1, 12))
    story.append(Paragraph("8. How to Run the Project (Step-by-Step)", h1_style))
    story.append(Paragraph("<b>Step 1 — Create MySQL Database:</b>", h2_style))
    story.append(make_code_box("mysql -u root -p\nCREATE DATABASE bookstore_db;"))
    
    story.append(Paragraph("<b>Step 2 — Verify Configuration (`application.properties`):</b>", h2_style))
    story.append(make_code_box(
        "spring.datasource.url=jdbc:mysql://localhost:3306/bookstore_db\n"
        "spring.datasource.username=root\n"
        "spring.datasource.password=root"
    ))

    story.append(Paragraph("<b>Step 3 — Build and Run the Application:</b>", h2_style))
    story.append(make_code_box(
        "# Windows PowerShell / Command Prompt:\n"
        ".\\mvnw clean compile\n"
        ".\\mvnw spring-boot:run\n\n"
        "# macOS / Linux:\n"
        "./mvnw clean compile\n"
        "./mvnw spring-boot:run"
    ))

    story.append(Paragraph("<b>Step 4 — Access the Web Application in Browser:</b>", h2_style))
    story.append(Paragraph("• <b>Customer Storefront:</b> <a href='http://localhost:8080/index.html'>http://localhost:8080/index.html</a>", bullet_style))
    story.append(Paragraph("• <b>Admin Portal:</b> <a href='http://localhost:8080/admin.html'>http://localhost:8080/admin.html</a>", bullet_style))

    # =========================================================================
    # 9. TECHNICAL INTERVIEW GUIDE & EXPLANATIONS
    # =========================================================================
    story.append(PageBreak())
    story.append(Paragraph("9. Technical Interview Questions & Answers", h1_style))
    story.append(Paragraph("Comprehensive, code-backed answers to the most frequent full-stack Spring Boot interview questions:", body_style))

    qa_list = [
        ("Q1: Explain your BookHub project.",
         "BookHub is an end-to-end full-stack bookstore web application built with Java 21, Spring Boot, Spring Data JPA, Hibernate, MySQL, and vanilla HTML5/CSS3/JavaScript. It includes customer-facing shopping with real-time stock checks, dynamic sliding cart drawer, atomic checkout with inventory decrement, and customer order history. For administrators, it offers book provisioning, cover image upload with client preview, and catalog deletion. The architecture is cleanly divided into Controller, Service, and Repository layers with centralized exception handling."),

        ("Q2: Why did you choose Spring Boot?",
         "Spring Boot eliminates the extensive XML and manual boilerplate configuration historically required in Spring. It provides opinionated auto-configuration, bundles an embedded Apache Tomcat web server (enabling execution as a self-contained JAR), and natively integrates with Spring Data JPA and HikariCP connection pooling."),

        ("Q3: Why MySQL for the database?",
         "BookHub manages purchasing transactions and inventory stock, requiring strict ACID guarantees and referential integrity. A relational database allows foreign key enforcement between cart items and books, ensures atomic updates during checkout, and prevents data anomalies."),

        ("Q4: Why JPA/Hibernate?",
         "JPA is the standard Java specification for Object-Relational Mapping (ORM), and Hibernate is its most robust implementation. It abstracts away manual JDBC ResultSet extraction and SQL string management, allowing developers to manipulate database tables as strongly-typed Java objects. Combined with Spring Data JPA, full CRUD operations are auto-generated without writing SQL queries."),

        ("Q5: Why REST APIs?",
         "REST is stateless, scalable, and decouples the client from the server. Communicating via standard HTTP verbs (GET, POST, DELETE) with JSON bodies enables any client (web browser, mobile app, or external system) to interact with the backend without server-side modifications."),

        ("Q6: Explain the MVC architecture in BookHub.",
         "BookHub implements MVC: Model consists of JPA entities (Book, CartItem, Order) and DTOs (ApiResponse); View comprises static web pages (index.html, admin.html); Controller is implemented by @RestController classes (BookController, CartController, OrderController) which handle HTTP requests, delegate to Services, and return JSON models."),

        ("Q7: Explain the complete request-to-response flow.",
         "When a user triggers an action (e.g. clicking 'Add to Cart'):\n1. Browser JavaScript issues an asynchronous HTTP request (e.g. POST /cart/1/2).\n2. Embedded Tomcat receives the socket request and passes it to DispatcherServlet.\n3. DispatcherServlet routes to CartController.add(id, qty).\n4. The controller delegates to CartService.addToCart(id, qty).\n5. CartService verifies stock via BookRepository and saves CartItem via CartRepository.\n6. Hibernate executes an SQL INSERT into MySQL via HikariCP.\n7. The controller wraps the saved entity in ApiResponse<CartItem>.\n8. Jackson serializes the ApiResponse into JSON and Tomcat returns HTTP 200 to the browser.\n9. The browser's Fetch promise resolves, and JavaScript updates the UI dynamically."),

        ("Q8: How does an order update stock?",
         "In OrderService.placeOrder(userId), the service queries all active cart items via cartRepo.findAll(). For each item, it verifies that item.quantity <= book.quantity, calculates item cost, decrements inventory stock (book.quantity - item.quantity), and commits the change via bookRepo.save(book). It then empties the cart with cartRepo.deleteAll() and saves an Order entity with the total cost and userId."),

        ("Q9: How does the cart work?",
         "The cart is backed by the cart_item MySQL table, which stores a foreign key (book_id) referencing the book table along with the chosen quantity. When an item is added, CartService checks that the book exists and has sufficient stock. The frontend cart drawer dynamically queries GET /cart to compute running totals and render line items."),

        ("Q10: How does the frontend communicate with the backend?",
         "Communication occurs exclusively through HTTP REST API calls using the browser's native Fetch API with async/await. Data is transmitted as JSON with Content-Type: application/json (or multipart/form-data for image uploads) to http://localhost:8080. @CrossOrigin enables smooth communication across origins."),

        ("Q11: Where does the application start?",
         "Execution begins in BookstoreApplication.java at public static void main(String[] args). SpringApplication.run() initializes the ApplicationContext, triggers component scanning across com.bookhub.bookstore, configures resource handlers, initializes Hibernate with MySQL, and starts Tomcat on port 8080."),

        ("Q12: What happens internally when an API is called?",
         "Tomcat assigns a worker thread from its thread pool to the incoming TCP connection. The request traverses servlet filters to DispatcherServlet, which maps the URL to the matching @RestController method. Request parameters and bodies are deserialized. The controller invokes the service layer, which performs business validation and executes database queries through Spring Data JPA repositories. The result is serialized to JSON by Jackson and written to the HTTP response stream."),

        ("Q13: What happens when a database operation fails?",
         "If a business constraint is violated (e.g. insufficient stock or non-existent book), the service throws a RuntimeException. Spring's @ControllerAdvice in GlobalExceptionHandler catches the exception and wraps it in a standardized ApiResponse(false, error_message, null) returning an HTTP 400 Bad Request status. For unexpected server errors, it catches generic Exception and returns HTTP 500, preventing stack trace leakage.")
    ]

    for q, a in qa_list:
        story.append(Paragraph(f"<b>{q}</b>", qa_q_style))
        story.append(Paragraph(a.replace('\n', '<br/>'), qa_a_style))

    # Build PDF with custom NumberedCanvas
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Successfully generated PDF: {filename}")

if __name__ == "__main__":
    out_pdf = "BookHub_Complete_Documentation_and_Interview_Guide.pdf"
    if len(sys.argv) > 1:
        out_pdf = sys.argv[1]
    build_pdf(out_pdf)
